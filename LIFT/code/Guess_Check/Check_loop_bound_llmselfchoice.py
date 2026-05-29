import os
import re
from utils import *
from functools import reduce
import subprocess
import signal
from CBC_Transform import CBChecker
from K_Transform import K_Transformer
from prompt_gen_llmselfchoice import *
import sys
import time
import logging
import yaml
import argparse
sys.path.append(os.path.abspath('code'))
from DataInfo import Task_Info

def extract_variables_from_bpl(bpl_file_path):
    """Extract all variable names from a BPL file using static analysis.
    
    Parses 'var' declarations in procedures to extract variable names.
    Example: 'var x,y,i: int;' -> ['x', 'y', 'i']
    
    Args:
        bpl_file_path: Path to the BPL file
        
    Returns:
        List of variable names found in the file
    """
    variables = []
    try:
        with open(bpl_file_path, 'r') as f:
            content = f.read()
        
        # Pattern to match variable declarations: var name1, name2, ...: type;
        # Handles multiple declarations and various types
        var_pattern = r'\bvar\s+([^;]+);'
        matches = re.findall(var_pattern, content)
        
        for match in matches:
            # Split by ':' to separate variable names from type
            parts = match.split(':')
            if len(parts) >= 1:
                var_names_part = parts[0]
                # Split by ',' to get individual variable names
                var_names = [v.strip() for v in var_names_part.split(',')]
                for var_name in var_names:
                    # Clean up the variable name (remove any extra whitespace)
                    var_name = var_name.strip()
                    if var_name and var_name not in variables:
                        variables.append(var_name)
    except Exception as e:
        print(f"Error extracting variables from {bpl_file_path}: {e}")
    
    return variables



class VerificationTimeoutError(RuntimeError):
    """Custom exception for verification timeouts."""
    def __init__(self, message="Boogie verification timed out"):
        self.message = message
        super().__init__(self.message)

class BoogieVerifier:
    def __init__(self, filename, tmpfile, learner='dt_penalty', project_dir=None, varlist=None):
        self.learner = learner
        self.project_dir = project_dir if project_dir else os.getcwd()
        self.boogie_dir = f"{self.project_dir}/ice/popl16_artifact/Boogie/Binaries"
        self.ReList = [r'(.*)%M:(.*)%(.*)',r'(.*)%Decl:(.*)%(.*)',r'(.*)%Inv:(.*)%(.*)']
        self.LexicalReList = [r'(.*)%FD%(.*)',r'(.*)%VD%(.*)',r'(.*)%BE%(.*)',r'(.*)%IC%(.*)',r'(.*)%BT%(.*)',r'(.*)%IT%(.*)']
        self.timeoutMonitor = '/usr/bin/timeout'
        self.timeout = 60
        self.stdout_lines = []
        self.next_is_inv = False
        self.fileName = filename
        self.tempfile = tmpfile
        self.start_time = 0
        self.end_time = 0
        self.time = 0
        self.inv_it = 0
        self.varlist = varlist if varlist else []
        self._active_process = None
        self._active_pgid = None
    
    def _launch_process(self, command):
        """Launch a process in a new process group for easier cleanup"""
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        self._active_process = process
        try:
            self._active_pgid = os.getpgid(process.pid)
        except Exception:
            self._active_pgid = None
        return process

    def _terminate_process_tree(self):
        """Terminate the entire process tree including child processes like z3, c5.0"""
        process = self._active_process
        pgid = self._active_pgid
        if not process and pgid is None:
            return
        try:
            if pgid is None and process:
                pgid = os.getpgid(process.pid)
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except Exception as e:
            print(f"Failed to terminate Boogie/Z3 process group: {e}")
        finally:
            self._active_process = None
            self._active_pgid = None
        # Best-effort fallback: also kill by process name to avoid orphans
        self._kill_related_processes()

    def _kill_by_name(self, name):
        """Brute-force kill processes by name (fallback if group kill misses)."""
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, _ = p.communicate()
        for line in out.decode().splitlines():
            if name in line:
                try:
                    pid = int(line.split(None, 1)[0])
                    os.kill(pid, signal.SIGKILL)
                except ProcessLookupError:
                    ...

    def _kill_related_processes(self):
        for name in ['z3', 'mono', 'c5.0']:
            self._kill_by_name(name)

    def ensure_varlist_contains(self, vars_to_add):
        if vars_to_add is None:
            return
        if not isinstance(self.varlist, list):
            self.varlist = []
        if isinstance(vars_to_add, str):
            vars_to_add = [vars_to_add]
        for v in vars_to_add:
            if v and v not in self.varlist:
                self.varlist.append(v)
    
    @staticmethod
    def ce_dict_to_string(ce_dict):
        """Convert counterexample dictionary to string format: 'x=1, y=0, i=0'"""
        if not ce_dict or not isinstance(ce_dict, dict):
            return None
        items = [f"{key}={value}" for key, value in ce_dict.items()]
        return ", ".join(items)
    
    @staticmethod
    def IsNumber(s):
        if not type(s) == str:
            raise RuntimeError('Only to judge a string object!')
        s = s.replace(' ','')
        if s == '':
            return False
        for i in range(len(s)):
            if ord(s[i]) - ord('0') in range(0, 9) or ord(s[i]) == ord('-') and i == 0:
                continue
            else:
                return False
        return True
    
    @staticmethod
    def Expr2ATTRName(expr):
        rename = expr.replace(' ','')
        rename = rename.replace('|','')
        rename = rename.replace('+','$ADD$')
        rename = rename.replace('-','$SUB$')
        rename = rename.replace('*','$MUL$')
        rename = rename.replace('div','$DIV$')
        rename = rename.replace('/','$DIV$')
        rename = rename.replace('(', '$LP$')
        rename = rename.replace(')', '$RP$')
        rename = 'ATTR$' + rename
        return rename
    
    def GenerateITCode(self, lexRank, itVars, now, indent=0, indentIC=2):
        if now == 0:
            return indent * ' ' + '{} := {} - 1;\n'.format(itVars[now], itVars[now])
        rankingBound = ''
        firstRanking = True
        # import pdb; pdb.set_trace()
        for it in lexRank[now]:
            if firstRanking:
                rankingBound += '{} >= {}'.format(itVars[now], it)
                firstRanking = False
            else:
                rankingBound += ' && {} >= {}'.format(itVars[now], it)

        Content = indent * ' ' + 'if(' + itVars[now] + ' > 0){\n' + \
                (indent + indentIC) * ' ' + '{} := {} - 1;\n'.format(itVars[now], itVars[now]) + \
                indent * ' ' + '}\n' + \
                indent * ' ' + 'else{\n' + \
                self.GenerateITCode(lexRank, itVars, now-1, indent+indentIC, indentIC) + \
                (indent + indentIC) * ' ' + 'havoc {};\n'.format(itVars[now]) + \
                (indent + indentIC) * ' ' + 'assume({});\n'.format(rankingBound) + \
                indent * ' ' + '}\n'
        return Content
    
    def GenerateConcreteBplFile(self, boundMList = []):
        # duplicate remove
        boundMList = list(set(boundMList))
        boundMList.sort(reverse=True)
        fileOpen = open(self.tempfile)

        outFileOpen = open(self.fileName, 'w')

        tempContent = fileOpen.readlines()
        fileOpen.close()
        for line in tempContent:
            for patternId in range(len(self.ReList)):
                pattern = self.ReList[patternId]
                result = re.search(pattern, line)
                if not result is None:
                    identifierI = result.group(2).replace(' ','')
                    subReplace = list(filter(lambda x: x[0]==identifierI, boundMList))
                    # if not (identifierI, '0') in subReplace:
                    #     subReplace.append((identifierI, '0'))
                    if patternId == 0:
                        #print('match M for:{}'.format(identifierI))
                        formula = ''
                        for subId in range(len(subReplace)):
                            formula += ('' if subId == 0 else ' && ') + identifierI + ' >= ' + subReplace[subId][1]#.replace(' ','')
                        outFileOpen.write(result.group(1) + formula + result.group(3) + '\n')
                    elif patternId == 1:
                        #print('match Decl for:{}'.format(identifierI))
                        args = ''
                        for subId in range(len(subReplace)):
                            if BoogieVerifier.IsNumber(subReplace[subId][1]):
                            # if subReplace[subId][1] == '1':
                                continue
                            rename = BoogieVerifier.Expr2ATTRName(subReplace[subId][1])
                            '''rename = subReplace[subId][1].replace(' ','')
                            rename = subReplace[subId][1].replace('|','')
                            rename = rename.replace('+','$ADD$')
                            rename = rename.replace('-','$SUB$')
                            rename = rename.replace('*','$MUL$')
                            #rename = rename.replace('/','$DIV$')
                            #rename = rename.replace('div','$DIV$')
                            rename = 'ATTR$' + rename'''

                            args += ', ' + rename + ':int'
                        outFileOpen.write(result.group(1) + args + result.group(3) + '\n')
                    else:
                        #print('match Inv for:{}'.format(identifierI))
                        args = ''
                        for subId in range(len(subReplace)):
                            if BoogieVerifier.IsNumber(subReplace[subId][1]):
                                continue
                            args += ', ' + subReplace[subId][1]
                        outFileOpen.write(result.group(1) + args + result.group(3) + '\n')
                    
                    break
                else:
                    if patternId == len(self.ReList) - 1:
                        outFileOpen.write(line)
        outFileOpen.close()

    # lexRank is a 2-dim list
    def GenerateConcreteBplFileLexicalTemplate(self, lexRank, itVar='i'):
        itVars = lex_counter_distill(lexRank, itVar)
        allLexical = []
        for i in range(len(lexRank)):
            # duplicate remove
            lexRank[i] = list(set(lexRank[i]))
            lexRank[i].sort(reverse=True)
            allLexical += lexRank[i]
        allLexical = list(set(allLexical))
        allLexical.sort(reverse=True)

        fileOpen = open(self.tempfile)
        outFileOpen = open(self.fileName, 'w')
        tempContent = fileOpen.readlines()
        fileOpen.close()

        for line in tempContent:
            for patternId in range(len(self.LexicalReList)):
                pattern = self.LexicalReList[patternId]
                result = re.search(pattern, line)
                if not result is None:
                    patternBefore = result.group(1)
                    patternAfter = result.group(2)
                    if patternId == 0: # FD
                        FD_Text = ''
                        for it in itVars:
                            FD_Text += ',{}:int'.format(it)
                        for it in allLexical:
                            if BoogieVerifier.IsNumber(it):
                                continue
                            FD_Text += ',{}:int'.format(BoogieVerifier.Expr2ATTRName(it))
                        # i in ATTM to i_x
                        ATTMList = re.findall(',(.*?):int', patternAfter)
                        ATTMListNew = []
                        for attm in ATTMList:
                            attm = attm.replace(' ','').replace('\t','')
                            items = attm.split('$')
                            if itVar in items:
                                for iv in itVars:
                                    nitems = [iv if x == itVar else x for x in items]
                                    ATTMListNew.append(reduce(lambda x,y: '{}${}'.format(x,y), nitems))
                            else:
                                ATTMListNew.append(reduce(lambda x,y: '{}${}'.format(x,y), items))
                        NewATTMStr = ''
                        for its in ATTMListNew:
                            NewATTMStr += ', ' + its + ':int'
                        NewATTMStr += '): bool;'
                       
                        newcontent = patternBefore + FD_Text + NewATTMStr
                    elif patternId == 1: #VD
                        VD_Text = ''
                        for it in itVars:
                            VD_Text += ',{}'.format(it)
                        newcontent = patternBefore + VD_Text + patternAfter
                    elif patternId == 2: #BE
                        BE_Ctx = ''
                        BE_First = True
                        for i in range(len(itVars)):
                            varName = itVars[i]
                            for it in lexRank[i]:
                                if BE_First:
                                    BE_First = False
                                    BE_Ctx += '{} >= {}'.format(varName, it)
                                else:
                                     BE_Ctx += ' && {} >= {}'.format(varName, it)
                        BE_Text = 'assume({});'.format(BE_Ctx)
                        newcontent = patternBefore + BE_Text + patternAfter
                    elif patternId == 3: #IC
                        IC_Text = ''
                        for it in itVars:
                            IC_Text += ',{}'.format(it)
                        for it in allLexical:
                            if BoogieVerifier.IsNumber(it):
                                continue
                            IC_Text += ',{}'.format(it)

                        # i in ATTM to i_x
                        # ATTMList = re.findall(',(.*?)', patternAfter)
                        ATTMList = patternAfter.replace(');','').split(',')
                        ATTMList.remove('')
                        ATTMListNew = []
                        # print(ATTMList)
                        for attm in ATTMList:
                            attm = attm.replace('+',' + ').replace('-',' - ').replace('*',' * ')
                            items = attm.split(' ')
                            # print(items)
                            if itVar in items:
                                for iv in itVars:
                                    nitems = [iv if x == itVar else x for x in items]
                                    ATTMListNew.append(reduce(lambda x,y: '{} {}'.format(x,y), nitems))
                            else:
                                ATTMListNew.append(reduce(lambda x,y: '{} {}'.format(x,y), items))
                        NewATTMStr = ''
                        for its in ATTMListNew:
                            NewATTMStr += ', ' + its
                        NewATTMStr += ');'
                        
                        newcontent = patternBefore + IC_Text + NewATTMStr
                    elif patternId == 4: #BT
                        BT_Text = 'assert({} > 0);'.format(itVars[0])
                        newcontent = patternBefore + BT_Text + patternAfter
                    elif patternId == 5: #IT
                        # import pdb; pdb.set_trace()
                        IT_Text = self.GenerateITCode(lexRank, itVars, len(itVars)-1, patternBefore.count(' '))
                        if patternBefore.strip() == '':
                            patternBefore = ''
                        else:
                            patternBefore += '\n'
                        if patternAfter.strip() == '':
                            patternAfter = ''
                        else:
                            patternAfter = '\n' + patternAfter
                        newcontent = patternBefore + IT_Text + patternAfter

                    outFileOpen.write(newcontent + '\n')
                    break
                else:
                    if patternId == len(self.LexicalReList) - 1:
                        outFileOpen.write(line)
        outFileOpen.close()
        
    def setup_command(self, k_file_name):
        """Setup the Boogie command with arguments"""
        boogie_args = [
            '/noinfer', 
            '/contractInfer', 
            f'/mlHoudini:{self.learner}',
            '/printAssignment', 
            '/trace'
        ]
        return ['mono', 'Boogie.exe'] + boogie_args + [k_file_name]

    def run_verification(self, k_file_name):
        """Run the Boogie verification process"""
        current_dir = os.path.abspath('.')
        command = self.setup_command(k_file_name)
        self.start_time = time.perf_counter()
        # Change to Boogie directory and run process
        os.chdir(self.boogie_dir)
        Timer = [self.timeoutMonitor, '--foreground', '--kill-after', '1', str(int(self.timeout) + 1)]
        process = self._launch_process(Timer + command)
        os.chdir(current_dir)

        # Process output
        try:
            self._process_output(process)
            process.wait()
            if process.returncode in (124, 137):  # timeoutMonitor exit code
                self._terminate_process_tree()
                return 3, None, None
            self.end_time = time.perf_counter()
            self.time = self.end_time - self.start_time
            # Analyze results
        except VerificationTimeoutError:
            self._terminate_process_tree()
            return 3, None, None
        try:
            ret, inv, ce = self._analyze_results(k_file_name)
        except RuntimeError as e:
            print(f"Error during analysis: {e}")
            return 4, None, None
        finally:
            # Ensure all children (z3, c5.0) are gone even after normal completion
            self._terminate_process_tree()
        return ret, inv, ce

    def _process_output(self, process):
        """Process the output from Boogie execution"""
        while process.poll() is None:
            cur_time = time.perf_counter()
            if cur_time - self.start_time > self.timeout:
                self._terminate_process_tree()
                raise VerificationTimeoutError()
            line = process.stdout.readline().decode().strip()
            if line.startswith('\n') or line == '':
                continue
                
            self.stdout_lines.append(line)
            if self.next_is_inv:
                print(f'[Info] Guess Inv #{self.inv_it}: {line}')
                self.inv_it += 1
                self.next_is_inv = False
            if line.startswith('{'):
                self.next_is_inv = True

    def _analyze_results(self, k_file_name):
        """Analyze the verification results and extract counterexamples"""
        if not self.stdout_lines:
            raise RuntimeError('No output from Boogie execution')
            
        result_line = self.stdout_lines[-1]
        inv_line = self.stdout_lines[-4] if len(self.stdout_lines) >= 4 else None
        
        print(result_line)
        
        # Try first pattern
        re_matcher = r'Boogie program verifier finished with (\d+) verified, (\d+) error(s)?'
        re_result = re.search(re_matcher, result_line)
        
        if re_result is None:
            # Try second pattern - Failed-Simp
            re_matcher = r'Boogie program verifier exited with error detected at (.*):(.*)'  
            re_result = re.search(re_matcher, result_line)
            
            if re_result is None:
                if 'parse errors' in result_line:
                    return 4, None, None
                print('Result: Verification Timeout')
                return 3, None, None

            # Extract counterexample for Failed-Simp
            print('Result: Failed-Simp-Error')
            simpError = list(re_result.group(2).split(','))
            print(simpError)
            
            # Extract counterexample using ErrorFinder
            ce = None
            if self.varlist:
                try:
                    from ErrorFinder import ErrorFinder
                    error = ErrorFinder.simpCounterexample(None, k_file_name, self.varlist, simpError)
                    # error format: [(valueDict, 1)]
                    if error and len(error) > 0:
                        ce_dict = error[0][0]  # Get the valueDict
                        ce = self.ce_dict_to_string(ce_dict)  # Convert to string
                        print(f'Extracted counterexample: {ce}')
                except Exception as e:
                    print(f'Failed to extract counterexample: {e}')
            
            return 2, None, ce
            
        verified_num = int(re_result.group(1))
        error_num = int(re_result.group(2))
        
        if error_num == 0:
            print('Result: Verified-Invariant')
            print(inv_line)
            return 1, inv_line, None
        else:
            # Failed case - extract counterexample from model
            print('Result: Failed')
            ce = None
            if self.varlist:
                try:
                    from ErrorFinder.ErrorFinder import ErrorFinder
                    # Load ErrorFinder and extract counterexample
                    ef = ErrorFinder.load(None, k_file_name, self.varlist)
                    error = ef.getErrorInput()
                    # error format: [(valueDict, traceLen), ...]
                    if error and len(error) > 0:
                        ce_dict = error[0][0]  # Get the first valueDict
                        ce = self.ce_dict_to_string(ce_dict)  # Convert to string
                        print(f'Extracted counterexample: {ce}')
                except Exception as e:
                    print(f'Failed to extract counterexample: {e}')
            
            return 2, None, ce

    def get_output_lines(self):
        """Get all output lines"""
        return self.stdout_lines
global count_success
count_success = 0
global count_failed
count_failed = 0
global count_timeout
count_timeout = 0
global count_error
count_error = 0
def match_log_string(log_dir, search_string, log_filename):
    log_file_path = os.path.join(log_dir, log_filename)
    last_occurrence = None
    search_string = search_string + ".bpl"
    try:
        with open(log_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                if search_string in line:
                    last_occurrence = line.strip()
        
        # If search_string was found, check the last occurrence
        if last_occurrence is not None:
            if "succeeded" in last_occurrence:
                global count_success
                count_success += 1
            if "failed" in last_occurrence:
                global count_failed
                count_failed += 1
            if "timed out" in last_occurrence:
                global count_timeout
                count_timeout += 1
            if "error" in last_occurrence:
                global count_error
                count_error += 1
            return True
        
        return False
    
    except FileNotFoundError:
        print(f"Error: File {log_file_path} not found")
        return False
    except Exception as e:
        print(f"Error reading file: {e}")
        return False

def load_config(config_path='config_1.yaml'):
    default_config = {
        'directories': {
            'tmp_dir': '/tmpfs/tmp',
            'input_dir': '/root/LIFT/experiment/benchmarks-Instrumented',
            'input_lex_dir': '/root/LIFT/experiment/benchmarks-Instrumented-Lexicographic'
        },
        'llm_feedback': {
            'use_full_history': False,
            'if_prompt_ce': True,
            'if_prompt_hint': True,
            'repeat_expansion': True
        },
        'logging': {
            'log_dir': 'logs',
            'log_filename': 'llmselfchoice_dpsk_thinking.log'
        },
        'output': {
            'result_filename': 'results/llmselfchoice_dpsk_thinking.txt'
        },
        'verification': {
            'max_iterations': 15,
            'timeout_per_verification': 60
        },
        'file_list': []
    }

    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)

        def deep_merge(base, override):
            if override is None:
                return base
            for key, value in override.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    deep_merge(base[key], value)
                else:
                    base[key] = value
            return base

        deep_merge(default_config, user_config)

    return default_config

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loop bound verification with LLM self-choice')
    parser.add_argument('--config', '-c', default='config_1.yaml',
                        help='Path to configuration file (default: config_1.yaml)')
    parser.add_argument('--log-filename',
                        help='Override log filename')
    args = parser.parse_args()

    config = load_config(args.config)
    if args.log_filename:
        config['logging']['log_filename'] = args.log_filename

    tmpDir = config['directories']['tmp_dir']
    inputdir = config['directories']['input_dir']
    input_lexdir = config['directories']['input_lex_dir']
    out_filename = config['output']['result_filename']
    log_dir = config['logging']['log_dir']
    log_filename = config['logging']['log_filename']
    use_full_history = config.get('llm_feedback', {}).get('use_full_history', False)
    if_prompt_ce = config.get('llm_feedback', {}).get('if_prompt_ce', True)
    if_prompt_hint = config.get('llm_feedback', {}).get('if_prompt_hint', True)
    repeat_expansion = config.get('llm_feedback', {}).get('repeat_expansion', True)
    max_iterations = config['verification'].get('max_iterations', 15)
    timeout_per_verification = config['verification'].get('timeout_per_verification', 60)

    file_list = config.get('file_list', [])

    if file_list:
        files_to_process = []
        for fname in file_list:
            full_path = os.path.join(inputdir, fname, fname + '.bpl')
            if os.path.exists(full_path):
                files_to_process.append((fname, full_path))
            else:
                print(f"Warning: File not found: {full_path}")
        print(len(files_to_process))
    else:
        boogie_files = find_bpl_files(inputdir)
        files_to_process = []
        for inputfile in boogie_files:
            last_slash_index = inputfile.rfind('/')
            fname = inputfile[last_slash_index + 1: -4]
            files_to_process.append((fname, inputfile))
        print(len(files_to_process))

    success_count = 0
    failure_count = 0
    time_out_count = 0
    error_count = 0
    result = []
    logger = setup_logging(log_dir, log_filename)
    
    # Create task name to varlist mapping
    task_varlist_map = {}
    for task_info in Task_Info:
        task_name = task_info[0]
        varlist = task_info[1] if len(task_info) > 1 else []
        task_varlist_map[task_name] = varlist
    
    for filename, inputfile in files_to_process:
        full_filename = filename + ".bpl"
        if match_log_string(log_dir, filename, log_filename):
            print(f"Skipping {filename} as it has already been processed")
            continue
        
        # Get varlist from DataInfo
        varlist = task_varlist_map.get(filename, [])
        print(f"Processing {filename} with varlist: {varlist}")
        
        iter_back = 0
        prompt_type = 0
        feed_back_message = ""
        ce = None  # counterexample
        repeat_notice = False
        itvar = 'i'
        boogie_code = read_file_to_string(inputfile)
        c_code = read_file_to_string_c(filename)
        verification_ret = 0
        previous_loop_bound = []
        previous_lexical_loop_bound = []
        previous_llm_answer = []  # Stores [llm_answer, prompt_type, CE] tuples
        # Maximum max_iterations iterations, exit on successful verification
        while(iter_back < max_iterations and verification_ret != 1):
            if previous_llm_answer:
                if use_full_history or repeat_notice:
                    # Extract all history as three separate lists
                    all_history_tmp = list(zip(*previous_llm_answer))
                    all_history = [list(item) for item in all_history_tmp]
                    # Don't unpack - pass the entire structure to maintain all three lists
                    feed_back_message = all_history  # [answers_list, types_list, ces_list]
                    # For type checking in generate_loop_bound_prompt, use the types_list
                    prompt_type = all_history[1]  # Keep as list for repeat_notice mode
                    ce = all_history[2]  # Keep as list for repeat_notice mode
                    # Force repeat_notice=True when use_full_history is enabled
                    if use_full_history:
                        repeat_notice = True
                else:
                    feed_back_message = previous_llm_answer[-1][0]
                    prompt_type = previous_llm_answer[-1][1]
                    ce = previous_llm_answer[-1][2]
            (llm_answer, infer_time, token_usage) = openai_gen_answer(boogie_code, prompt_type, feed_back_message, repeat_notice=repeat_notice, if_prompt_ce=if_prompt_ce, if_prompt_hint=if_prompt_hint)
            
            # Check if LLM call failed (all retries exhausted)
            if llm_answer is None:
                logger.error(f"LLM API call failed after all retries for file: {full_filename}")
                print(f"LLM API call failed after all retries for file: {full_filename}")
                break  # Exit the iteration loop for this file
            
            parsed_output = parse_llm_loop_bound_output_lenient(llm_answer)
            if parsed_output is None:
                logger.info(f"Format error with the loop bound: {llm_answer}, file: {full_filename} , infer_time: {infer_time}, feed_back_iter: {iter_back}")
                feedback_msg = f"{llm_answer}. Format error: Your output does not follow the required format 'loop bound type: T, content: \'assume(...)\''. Please ensure you provide both the type and the content correctly."
                previous_llm_answer.append([feedback_msg, 1, None])
                iter_back += 1
                continue
            
            type_id, llm_answer = parsed_output
            if type_id == 0: 
                origin_file = inputdir + "/" + filename + "/" +full_filename
                llm_answer = remove_empty(llm_answer)
                #feed_back_message[0] = llm_answer
                loop_bound, llm_answer = extract_assume_expressions(llm_answer)
                if loop_bound in previous_loop_bound:
                    print(f"Loop bound {llm_answer} has already been tried.")
                    logger.info(f"Loop bound {llm_answer} has already been tried.")
                    if repeat_expansion:
                        repeat_notice = True
                    iter_back += 1
                    continue
                repeat_notice = False
                # If the right side contains a counter, skip to the next generation iteration
                i_break_flag = False
                for bound in loop_bound:
                    pattern = r'\bi\b'
                    if re.search(pattern, bound[1]):
                        i_break_flag = True
                        prompt_type = 1
                        break
                if i_break_flag:
                    prompt_type = 1
                    logger.info(f"Counter error with the loop bound: {llm_answer}, file: {full_filename} , infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                    previous_llm_answer.append([str(llm_answer), prompt_type, None])
                    iter_back += 1
                    continue
                previous_loop_bound.append(loop_bound)
                #llm_answer = "assume(i >= 0);"
            elif type_id == 1:
                origin_file = input_lexdir + "/" + filename + "/" + full_filename
                llm_answer = remove_empty(llm_answer)
                #feed_back_message[0] = llm_answer
                lexical_loop_bound, llm_answer = extract_lexical_bounds(llm_answer)
                if lexical_loop_bound in previous_lexical_loop_bound:
                    print(f"Lexical loop bound {llm_answer} has already been tried.")
                    logger.info(f"Lexical loop bound {llm_answer} has already been tried.")
                    if repeat_expansion:
                        repeat_notice = True
                    iter_back += 1
                    continue
                repeat_notice = False
                # If the right side contains a counter, skip to the next generation iteration
                # 1. Build a list containing all possible counters (i1, i2, ...) outside the loop
                num_counters = len(lexical_loop_bound)
                search_terms = [f'i{j}' for j in range(num_counters)]
                search_terms.append('i')
                # 2. Join all search terms with '|' and compile into a regex pattern
                # Format: r'\b(i1|i2|...|iN)\b'
                combined_pattern_str = r'\b(' + '|'.join(search_terms) + r')\b'
                compiled_pattern = re.compile(combined_pattern_str)

                # 3. Use any() with a generator expression for a single-pass check.
                #    - Iterates through all bounds, returns True immediately if any match is found.
                if any(compiled_pattern.search(bound) for counter in lexical_loop_bound for bound in counter):
                    prompt_type = 1
                    logger.info(f"Counter error with the loop bound: {llm_answer}, file: {full_filename} , infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                    previous_llm_answer.append([str(llm_answer), prompt_type, None])
                    iter_back += 1       
                    continue
                previous_lexical_loop_bound.append(lexical_loop_bound)
            k_Transformer = K_Transformer(tmpDir, origin_file, itvar)
            # Use varlist from Task_Info if available, otherwise extract from bpl file
            base_varlist = varlist[:] if varlist else extract_variables_from_bpl(origin_file)
            verifier = BoogieVerifier(k_Transformer.fileName, origin_file, learner='dt_penalty', varlist=base_varlist)
            verifier.timeout = timeout_per_verification
            if type_id == 0:
                verifier.ensure_varlist_contains(itvar)
                verifier.GenerateConcreteBplFile(loop_bound)
                if len(loop_bound) == 1:
                    simple_bound = loop_bound[0][1]
                    if not BoogieVerifier.IsNumber(simple_bound):
                        # Non-number (including empty string) treated as format error, prompt LLM for valid constant
                        print(f"Loop bound constant is not a number: '{simple_bound}'. Skipping and requesting new bound.")
                        logger.info(f"Loop bound constant is not a number: '{simple_bound}'. File: {full_filename}, llm_answer: {llm_answer}, infer_time: {infer_time}, feed_back_iter: {iter_back}")
                        prompt_type = 1
                        previous_llm_answer.append([str(llm_answer), prompt_type, None])
                        iter_back += 1
                        continue
                    if BoogieVerifier.IsNumber(simple_bound):
                        simple_bound = int(simple_bound)
                        if simple_bound < 100000: # CBC unrolling should not be too large
                            cbcchecker = CBChecker(tmpDir, k_Transformer.fileName, itvar)
                            cbc_ret = cbcchecker.ExecuteCBC(simple_bound, timeout=60, timeoutMonitor='/usr/bin/timeout')
                            if cbc_ret == 1:
                                print(f"Verification succeeded with the loop bound: {llm_answer}, invariant: CBC Bound-- {simple_bound}")
                                logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, invariant: CBC Bound-- {simple_bound}, k: 0, invariant: None, verification_time: {cbcchecker.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                                success_count += 1
                                verification_ret = 1
                                break
                            elif cbc_ret == 2:
                                print("CBC verification failed")
                                logger.info(f"CBC verification failed with the loop bound: {llm_answer}, file: {full_filename} , k: 0, feed_back_iter: {iter_back}, verification_time: {cbcchecker.time}, infer_time: {infer_time}, tokens: {token_usage['total_tokens']}")
                                simple_bound = simple_bound + 3 # try const added
                                cbc_ret = cbcchecker.ExecuteCBC(simple_bound, timeout=timeout_per_verification, timeoutMonitor='/usr/bin/timeout')
                                if cbc_ret == 1:
                                    print(f"Verification succeeded with the loop bound: {llm_answer}, const_part: 3, invariant: CBC Bound-- {simple_bound}")
                                    logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, invariant: CBC Bound-- {simple_bound}, k: 0, invariant: None, verification_time: {cbcchecker.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, const_part: 3, tokens: {token_usage['total_tokens']}")
                                    success_count += 1
                                    verification_ret = 1
                                    break
                                elif cbc_ret == 2:
                                    print("CBC verification failed after adding const")
                                    logger.info(f"CBC verification failed after adding const with the loop bound: {llm_answer}, file: {full_filename} , k: 0, feed_back_iter: {iter_back}, verification_time: {cbcchecker.time}, infer_time: {infer_time}, const_part: 3, tokens: {token_usage['total_tokens']}")
                                    prompt_type = 2
                                    previous_llm_answer.append([str(llm_answer), prompt_type, None])
                                    iter_back += 1
                                    continue
                                elif cbc_ret == 3:
                                    print("CBC verification timed out after adding const")
                                    logger.info(f"CBC verification timed out after adding const with the loop bound: {llm_answer}, file: {full_filename} , k: 0, feed_back_iter: {iter_back}, verification_time: {cbcchecker.time}, infer_time: {infer_time}, const_part: 3, tokens: {token_usage['total_tokens']}")
                            prompt_type = 3
                            previous_llm_answer.append([llm_answer, prompt_type, None])
                            iter_back += 1
                            continue
                k = 1
                while(k <= 3):
                    try:
                        k_Transformer.GenerateConcreteBplFile(k, withinv=True)
                    except RuntimeError as e:
                        print(f"Error during k-transformer: {e}")
                        logger.info(f"K-transformer error with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        break
                    except IndexError as e:
                        print(f"Error during k-transformer: {e}")
                        logger.info(f"K-transformer error with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        break
                    try:
                        verification_ret, invariant, ce = verifier.run_verification(k_Transformer.K_fileName)
                        if verification_ret == 1:
                            print(f"Verification succeeded with the loop bound: {llm_answer}, invariant: {invariant}")
                            logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, invariant: {invariant}, verification_time: {verifier.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                            success_count += 1
                            break
                        elif verification_ret == 2:
                            print("Verification failed")
                            logger.info(f"Verification failed with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, verification_time: {verifier.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                            if k == 1:
                                prompt_type = 2
                                previous_llm_answer.append([llm_answer, prompt_type, ce])
                        elif verification_ret == 3:
                            print("Verification timed out")
                            logger.info(f"Verification timed out with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                            if k == 1:
                                prompt_type = 3
                                previous_llm_answer.append([llm_answer, prompt_type, None])
                        elif verification_ret == 4:
                            print("ICE Runtime error")
                            logger.info(f"ICE Runtime error with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, verification_time: {verifier.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                            if k == 1:
                                prompt_type = 1
                                previous_llm_answer.append([llm_answer, prompt_type, None])
                            break
                    except RuntimeError as e:
                        print(f"Error during verification: {e}")
                    if k == 3:
                        new_loop_bound = []
                        for bound in loop_bound:
                            new_bound = (bound[0], bound[1] + '+3')
                            new_loop_bound.append(new_bound)
                        verifier.GenerateConcreteBplFile(new_loop_bound)
                        k_Transformer.GenerateConcreteBplFile(1, withinv=True)
                        verification_ret, invariant, ce = verifier.run_verification(k_Transformer.K_fileName)
                        if verification_ret == 1:
                            print(f"Verification succeeded with the loop bound: {llm_answer}, const_part: 3, invariant: {invariant}")
                            logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, invariant: {invariant}, verification_time: {verifier.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, const_part: 3, tokens: {token_usage['total_tokens']}")
                            success_count += 1
                        else:
                            status_map = {2: "failed", 3: "timed out", 4: "ICE runtime error"}
                            status_text = status_map.get(verification_ret, "unknown result")
                            print(f"Const-add verification {status_text} with loop bound: {llm_answer}, const_part: 3")
                            logger.info(
                                f"Const-add verification {status_text} with the loop bound: {llm_answer}, file: {full_filename}, "
                                f"const_part: 3, verification_time: {verifier.time}, infer_time: {infer_time}, "
                                f"feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}"
                            )
                    k += 1
            elif type_id == 1:
                itVars = lex_counter_distill(lexical_loop_bound, itvar)
                if not itVars:
                    print(f"Error during lexicographic loop bound format with this answer: {llm_answer}")
                    logger.info(f"Error during lexicographic loop bound format with this answer: {llm_answer}, file: {full_filename}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                    prompt_type = 1
                    previous_llm_answer.append([str(llm_answer), prompt_type, None])
                    iter_back += 1
                    continue
                verifier.ensure_varlist_contains(itVars)
                verifier.GenerateConcreteBplFileLexicalTemplate(lexical_loop_bound)
                #k_Transformer.GenerateConcreteBplFile(1)
                k = 1
                const_part = 0
                while(k <= 3):
                    try:
                        k_Transformer.GenerateConcreteBplFileLexical(k, itVars, withinv=True)
                    except RuntimeError as e:
                        print(f"Error during k-transformer: {e}")
                        logger.info(f"K-transformer error with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        break
                    except IndexError as e:
                        print(f"Error during k-transformer: {e}")
                        logger.info(f"K-transformer error with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        break
                    try:
                        verification_ret, invariant, ce = verifier.run_verification(k_Transformer.K_fileName)
                        if verification_ret == 1:
                            print(f"Verification succeeded with the loop bound: {llm_answer}, invariant: {invariant}")
                            logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, invariant: {invariant}, verification_time: {verifier.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                            success_count += 1
                            break
                        elif verification_ret == 2:
                            print("Verification failed")
                            logger.info(f"Verification failed with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, feed_back_iter: {iter_back}, verification_time: {verifier.time}, infer_time: {infer_time}, tokens: {token_usage['total_tokens']}")
                            if k == 1:
                                prompt_type = 2
                                previous_llm_answer.append([llm_answer, prompt_type, ce])
                        elif verification_ret == 3:
                            print("Verification timed out")
                            logger.info(f"Verification timed out with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                            if k == 1:
                                prompt_type = 3
                                previous_llm_answer.append([llm_answer, prompt_type, None])
                        elif verification_ret == 4:
                            print("ICE Runtime error")
                            logger.info(f"ICE Runtime error with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, infer_time: {infer_time}, verification_time: {verifier.time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                            if k == 1:
                                prompt_type = 1
                                previous_llm_answer.append([llm_answer, prompt_type, None])
                            break
                    except RuntimeError as e:
                        print(f"Error during verification: {e}")
                    if k == 3:
                        new_lexi_loop_bound = []
                        new_lexi_counter = []
                        for counter in lexical_loop_bound:
                            for bound in counter:
                                bound = bound + '+3'
                                new_lexi_counter.append(bound)
                            new_lexi_loop_bound.append(new_lexi_counter)
                        verifier.GenerateConcreteBplFileLexicalTemplate(new_lexi_loop_bound)
                        k_Transformer.GenerateConcreteBplFileLexical(1, itVars, withinv=True)
                        verification_ret, invariant, ce = verifier.run_verification(k_Transformer.K_fileName)
                        if verification_ret == 1:
                            print(f"Verification succeeded with the loop bound: {llm_answer}, const_part: 3, invariant: {invariant}")
                            logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, invariant: {invariant}, verification_time: {verifier.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, const_part: 3, tokens: {token_usage['total_tokens']}")
                            success_count += 1
                        else:
                            status_map = {2: "failed", 3: "timed out", 4: "ICE runtime error"}
                            status_text = status_map.get(verification_ret, "unknown result")
                            print(f"Const-add lexical verification {status_text} with loop bound: {llm_answer}, const_part: 3")
                            logger.info(
                                f"Const-add lexical verification {status_text} with the loop bound: {llm_answer}, file: {full_filename}, "
                                f"const_part: 3, verification_time: {verifier.time}, infer_time: {infer_time}, "
                                f"feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}"
                            )
                    k += 1
            iter_back += 1
    success_count += count_success
    failure_count += count_failed
    time_out_count += count_timeout
    error_count += count_error
    print(f"Count of succeeded: {success_count}")
    print(f"Count of failed: {failure_count}")
    print(f"Count of timed out: {count_timeout}")
    print(f"Count of error: {count_error}")
    with open(out_filename, 'w', encoding='utf-8') as f:
        f.write(f"Success count: {success_count}\n")
        f.write(f"Failure count: {failure_count}\n")
        f.write(f"Timeout count: {time_out_count}\n")
        f.write(f"Error count: {error_count}\n")


