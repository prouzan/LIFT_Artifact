import os
import re
from utils import *
from functools import reduce
import signal
import subprocess
from K_Transform import K_Transformer
from CBC_Transform import CBChecker
from ReInvariantChecker import ReInvariantChecker
from prompt_gen_newiter import *
import spilit
import sys
import time
import logging
import yaml
import argparse
sys.path.append(os.path.abspath('code'))

RESULT_TIMEOUT = 0
RESULT_VERIFIED = 1
RESULT_ERROR = 2
RESULT_INV_FAILED_HOLD = 3
RESULT_INV_FAILED_MAINTAIN = 4
RESULT_ASSERT_FAILED_HOLD = 5
RESULT_INV_ERROR = 6


def load_config(config_path='config.yaml'):
    """Load configuration from YAML file."""
    default_config = {
        'llm_lb': {'type': 0},
        'llm_invariant': {'type': 0},
        'directories': {
            'tmp_dir': '/tmpfs/tmp',
            'input_dir': '/root/LIFT/experiment/benchmarks-Instrumented',
            'input_lex_dir': '/root/LIFT/experiment/benchmarks-Instrumented-Lexicographic'
        },
        'logging': {
            'log_dir': 'logs',
            'log_filename': 'gemini_gpt_invariant.log'
        },
        'output': {
            'result_filename': 'results/gemini_gpt_invariant.txt'
        },
        'verification': {
            'max_conj_iterations': 5,
            'max_lex_iterations': 15,
            'k_induction_max': 3,
            'timeout_per_verification': 60
        },
        'file_list': []
    }
    
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            user_config = yaml.safe_load(f)
        
        # Deep merge user config into default config
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

class VerificationTimeoutError(RuntimeError):
    """Custom exception for verification timeouts."""
    def __init__(self, message="Boogie verification timed out"):
        self.message = message
        super().__init__(self.message)

class BoogieVerifier:
    def __init__(self, filename, tmpfile, learner='dt_penalty', project_dir=None):
        self.learner = learner
        self.project_dir = project_dir if project_dir else os.getcwd()
        self.boogie_dir = f"{self.project_dir}/ice/popl16_artifact/Boogie/Binaries"
        self.ReList = [r'(.*)%M:(.*)%(.*)',r'(.*)%Decl:(.*)%(.*)',r'(.*)%Inv:(.*)%(.*)']
        self.LexicalReList = [r'(.*)%FD%(.*)',r'(.*)%VD%(.*)',r'(.*)%BE%(.*)',r'(.*)%IC%(.*)',r'(.*)%BT%(.*)',r'(.*)%IT%(.*)']
        self.timeoutMonitor = '/usr/bin/timeout'
        self.verified_timeout = 60
        self.stdout_lines = []
        self.fileName = filename
        self.tempfile = tmpfile
        self.invariant_infer_time = 0
        self.invariant_infer_freq = 0
        self.invariant_verified_time = 0
        self.invariant_verified_freq = 0
        self.invariant_time = 0
        self.com_invariant_verified_freq = 0
    
    @staticmethod
    def IsNumber(s):
        if not type(s) == str:
            raise RuntimeError('Only to judge a string object!')
        s = s.replace(' ','')
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
        line_counter = 0
        for line in tempContent:
            line_counter += 1
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
                    elif patternId == 1 and line_counter > 1:
                        #print('match Decl for:{}'.format(identifierI))
                        args = ''
                        for subId in range(len(subReplace)):
                            if BoogieVerifier.IsNumber(subReplace[subId][1]):
                            # if subReplace[subId][1] == '1':
                                continue
                            rename = BoogieVerifier.Expr2ATTRName(subReplace[subId][1])
                            args += ', ' + rename + ':int'
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

        for line_counter, line in enumerate(tempContent):
            for patternId in range(len(self.LexicalReList)):
                pattern = self.LexicalReList[patternId]
                result = re.search(pattern, line)
                newcontent = ""
                if not result is None and line_counter > 1:
                    patternBefore = result.group(1)
                    patternAfter = result.group(2)
                    if patternId == 1: #VD
                        VD_Text = ''
                        for it in itVars:
                            VD_Text += ',{}'.format(it)
                        newcontent = patternBefore + VD_Text + patternAfter
                        # If this reconstructed line is a var declaration, remove TR* items and preserve group type if present
                        m = re.match(r'^(\s*)var\s+(.*?);\s*$', newcontent)
                        if m:
                            _indent = m.group(1)
                            _body = m.group(2)
                            _parts = [p.strip() for p in _body.split(',') if p.strip() != '']
                            # Detect group type pattern: only the last part has ': type' and previous ones don't
                            _group_type = None
                            if _parts:
                                _typed_flags = [(':' in p) for p in _parts]
                                if _typed_flags.count(True) == 1 and _typed_flags[-1] and all(not f for f in _typed_flags[:-1]):
                                    _group_type = _parts[-1].split(':', 1)[1].strip()
                                
                            _kept_names_with_types = []
                            for p in _parts:
                                _name, _type = (p.split(':', 1)[0].strip(), p.split(':', 1)[1].strip()) if (':' in p) else (p.strip(), None)
                                if re.match(r'^TR\w*$', _name):
                                    continue
                                if _type is not None:
                                    _kept_names_with_types.append(f"{_name}: {_type}")
                                elif _group_type is not None:
                                    _kept_names_with_types.append(f"{_name}: {_group_type}")
                                else:
                                    _kept_names_with_types.append(_name)
                            if _kept_names_with_types:
                                newcontent = f"{_indent}var " + ', '.join(_kept_names_with_types) + ";"
                            else:
                                newcontent = ''
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
                        newcontent = " "
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
                    if patternId == len(self.LexicalReList) - 1 and line_counter > 1:
                        filtered_line = line

                        segments = [seg for seg in re.split(r';', filtered_line)]
                        kept_segments = []
                        for seg in segments:
                            seg_strip = seg.strip()
                            if seg_strip == '':
                                continue
                            if re.match(r'^\s*TR\w*\s*:=', seg_strip):
                                continue
                            kept_segments.append(seg.rstrip())

                        if kept_segments:
                            reconstructed = ';'.join(kept_segments)
                            if filtered_line.rstrip().endswith(';'):
                                reconstructed = reconstructed + ';'
                            indent_match = re.match(r'^(\s*)', filtered_line)
                            indent = indent_match.group(1) if indent_match else ''
                            filtered_line = indent + reconstructed + ('\n' if not reconstructed.endswith('\n') else '')
                        else:
                            filtered_line = ''

                        if filtered_line:
                            decl_match = re.match(r'^(\s*)var\s+(.*?);\s*\n?$', filtered_line)
                            if decl_match:
                                indent = decl_match.group(1)
                                decl_body = decl_match.group(2)
                                parts = [p.strip() for p in decl_body.split(',') if p.strip() != '']
                                # Detect group type like 'x, y, TR1, TR2: int'
                                group_type = None
                                if parts:
                                    typed_flags = [(':' in p) for p in parts]
                                    if typed_flags.count(True) == 1 and typed_flags[-1] and all(not f for f in typed_flags[:-1]):
                                        group_type = parts[-1].split(':', 1)[1].strip()
                                kept_items = []
                                for p in parts:
                                    if ':' in p:
                                        name, typ = p.split(':', 1)
                                        name = name.strip()
                                        typ = typ.strip()
                                    else:
                                        name = p.strip()
                                        typ = None
                                    if re.match(r'^TR\w*$', name):
                                        continue
                                    if typ is not None:
                                        kept_items.append(f"{name}: {typ}")
                                    elif group_type is not None:
                                        kept_items.append(f"{name}: {group_type}")
                                    else:
                                        kept_items.append(name)
                                if kept_items:
                                    filtered_line = f"{indent}var " + ', '.join(kept_items) + ";\n"
                                else:
                                    filtered_line = ''

                        if filtered_line:
                            outFileOpen.write(filtered_line)
            
        outFileOpen.close()

    def setup_command(self, file_name):
        """Setup the Boogie command with arguments"""
        smt_file = file_name[0: -4] + '.smt'
        boogie_args = [
            '/noinfer', 
            '/contractInfer', 
            #f'/mlHoudini:{self.learner}',
            f'/proverLog:{smt_file}',
            '/printAssignment', 
            '/printModel:4',
            '/trace'
        ]
        return ['mono', 'Boogie.exe'] + boogie_args + [file_name]

    def invariant_infer(self, filename, loop_bound, conj_or_lex, prompt_type, itVars=None, llm_type=0):
        AnsSet = []
        time_limit = 180 ##
        current_invariant_time = 0
        #self.invariant_time = 0
        tmpDir = '/tmpfs/tmp'
        full_filepath = tmpDir + '/' + filename
        bmc_Transformer = CBChecker(tmpDir, filename, 'i')
        k_Transformer = K_Transformer(tmpDir, filename, 'i')
        k_file_name = k_Transformer.K_fileName
        results = []
        results_bf_ktrans = []
        result = -1
        CounterExamples = []
        CounterExamples_bf_ktrans = []
        previous_invariants = []
        retry_count = 0
        code_with_bound = read_concret_file2string(filename)
        invariant = ""
        invariant_start_time = time.perf_counter()
        repeat_notice = False
        while result != RESULT_VERIFIED and result != RESULT_ERROR and current_invariant_time <= time_limit and retry_count <= 3:
            k = 0
            prompt_type = results_bf_ktrans
            (llm_answer, infer_time) = openai_gen_answer(1, llm_type, code_with_bound, conj_or_lex, prompt_type, invariant, CounterExamples_bf_ktrans, repeat_notice)
            self.invariant_infer_time += infer_time
            self.invariant_infer_freq += 1
            invariant = extract_invariant_statements(llm_answer)
            if invariant in previous_invariants:
                print(f"Invariant {invariant} has already been tried.")
                retry_count += 1
                repeat_notice = True
                continue
            repeat_notice = False
            previous_invariants.append(invariant)
            if invariant is None:
                result = RESULT_INV_ERROR
                invariant = llm_answer
                continue
            print("Inferred Invariant: {}".format(invariant))
            continue_flag = False
            break_flag = False
            #while (len(results) == 0 or RESULT_INV_FAILED_MAINTAIN in results or RESULT_INV_FAILED_HOLD in results or RESULT_TIMEOUT in results or RESULT_ERROR in results) and k <= 3:
            while k < 3:
                k += 1
                if k == 1:
                    results_bf_ktrans, CounterExamples_bf_ktrans = self.run_verification(full_filepath, invariant)
                    results = results_bf_ktrans
                    CounterExamples = CounterExamples_bf_ktrans
                else:
                    remove_invariant_lines(full_filepath)
                    if not conj_or_lex:
                        k_Transformer.GenerateConcreteBplFile(k)
                    else:
                        k_Transformer.GenerateConcreteBplFileLexical(k, itVars)
                    results, CounterExamples = self.run_verification(k_file_name, invariant)
                self.invariant_verified_freq += 1
                if results[0] == RESULT_VERIFIED:
                    result = RESULT_VERIFIED
                    break
                if results[0] == RESULT_INV_ERROR:
                    result = RESULT_INV_ERROR
                    break
                if results[0] == RESULT_ERROR:
                    result = RESULT_ERROR
                    break
            if len(results_bf_ktrans) == 1:
                result = results_bf_ktrans[0]
                if result == RESULT_VERIFIED:
                    invariant_end_time = time.perf_counter()
                    current_invariant_time = invariant_end_time - invariant_start_time
                    break
                if result == RESULT_TIMEOUT:
                    print("Timeout when verifying file: {} with invariant: {}".format(k_file_name, invariant))
                    invariant_end_time = time.perf_counter()
                    current_invariant_time = invariant_end_time - invariant_start_time
                    if current_invariant_time > time_limit:
                        break
                if result == RESULT_ERROR:
                    print("Error when verifying file: {} with loop_bound: {}".format(k_file_name, loop_bound))
                    invariant_end_time = time.perf_counter()
                    current_invariant_time = invariant_end_time - invariant_start_time
                    break
                if result == RESULT_INV_ERROR:
                    print("Error when verifying file: {} with invariant: {}".format(k_file_name, invariant))
                    invariant_end_time = time.perf_counter()
                    current_invariant_time = invariant_end_time - invariant_start_time
                    continue
                if result == RESULT_ASSERT_FAILED_HOLD:
                    print("Assertion failed to hold when verifying file: {} with invariant: {}".format(full_filepath, invariant))
                    smt_file = full_filepath[0: -4] + '.smt'
                    rechecker = ReInvariantChecker('/tmpfs/tmp', full_filepath, smt_file, 'i', conj_or_lex, self.boogie_dir, invariant, loop_bound, k, log_file = './logs/rechecker_logs/new_extract_ce_noind.log')
                    max_bound = 30
                    error_from_loopbound = rechecker.run_analysis(CounterExamples_bf_ktrans[0], max_bound=max_bound, conj_or_lexical=conj_or_lex)
                    if error_from_loopbound == 2:
                        print(f"Program verified by CBC within loop bound {max_bound}, terminating within {max_bound} iterations.")
                        invariant_end_time = time.perf_counter()
                        current_invariant_time = invariant_end_time - invariant_start_time
                        result = RESULT_VERIFIED
                        invariant = "CBC Bound-- " + str(max_bound)
                        break
                    elif isinstance(error_from_loopbound, tuple) and error_from_loopbound[0] == 1:
                        print("This failure is caused by the loop bound")
                        invariant_end_time = time.perf_counter()
                        current_invariant_time = invariant_end_time - invariant_start_time
                        # Use the real counterexample state (variable assignments from assume statements)
                        CE = error_from_loopbound[1]
                        break
                    elif error_from_loopbound == 1:
                        # Compatible with old version return format
                        print("This failure is caused by the loop bound")
                        invariant_end_time = time.perf_counter()
                        current_invariant_time = invariant_end_time - invariant_start_time
                        CE = CounterExamples_bf_ktrans[0]
                        break
                    else:
                        inv_file = full_filepath[0: -4] + "_inv.bpl"
                        remove_assert_lines(full_filepath, inv_file)
                        inv_results, inv_CounterExamples = self.run_verification(inv_file, invariant)
                        assert RESULT_ERROR not in inv_results and RESULT_INV_ERROR not in inv_results, "Error when verifying invariant alone"
                        assert RESULT_ASSERT_FAILED_HOLD not in inv_results, "Assertion should not fail when verifying invariant alone"
                        if inv_results[0] == RESULT_TIMEOUT:
                            print("Timeout when verifying invariant alone file: {} with invariant: {}".format(full_filepath, invariant))
                            result = RESULT_TIMEOUT
                        elif inv_results[0] != RESULT_VERIFIED:
                            results_bf_ktrans = inv_results + results_bf_ktrans
                            CounterExamples_bf_ktrans = inv_CounterExamples + CounterExamples_bf_ktrans
                        elif inv_results[0] == RESULT_VERIFIED:
                            AnsSet.append(invariant[10:-2].strip())
                            invariant_end_time = time.perf_counter()
                            current_invariant_time = invariant_end_time - invariant_start_time
                            continue
            print("Failed to verify file: {} with invariant: {}".format(full_filepath, invariant))
            remove_invariant_lines(full_filepath)
            print("-------BMC Verification for sub-invariants-------")
            invariantlist, outer_operator = spilit.split_invariant_predicates(invariant)
            print("invariantlist: {}, outer_operator: {}".format(invariantlist, outer_operator))
            lengthAnsSetbefore=len(AnsSet)
            if outer_operator == '||':
                ifaddall = self.BMC_and(bmc_Transformer, invariant, conj_or_lex)
                if ifaddall:
                    tempansset=[]
                    for subassertion in invariantlist:
                        if subassertion and subassertion not in tempansset and subassertion not in AnsSet:
                            subinvariant = "invariant !( " + subassertion + " );"
                            ifAdd = self.BMC_or(bmc_Transformer, subinvariant, conj_or_lex)
                            if ifAdd:
                                tempansset.append(subassertion)
                            else:
                                print("Discard subinvariant: {}".format(subinvariant))
                    resans=""
                    for res in tempansset:
                        resans = resans+"("+res+")"+"||"
                    if resans[0:-2] not in AnsSet and resans[0:-2] != "":
                        AnsSet.append(resans[0:-2])
                print("AnsSet: {}".format(AnsSet))
            else:
                for subassertion in invariantlist:
                    if subassertion and subassertion not in AnsSet : #and undefined_function(subassertion):
                        subinvariant = "invariant " + subassertion + ";"
                        ifAdd = self.BMC_and(bmc_Transformer, subinvariant, conj_or_lex)
                        if ifAdd and subassertion != "":
                            AnsSet.append(subassertion)
                        else:
                            print("Discard subinvariant: {}".format(subinvariant))
                print("AnsSet: {}".format(AnsSet))
            lengthAnsSetafter = len(AnsSet)
            AnsSetChanged = (lengthAnsSetafter != lengthAnsSetbefore)
            if AnsSetChanged:
                print("=================Combine Verifivation Begin=================")
                combine_invariant = join_with_proper_parentheses(AnsSet)
                combine_invariant = "invariant " + combine_invariant + ";"
                com_k = 0
                while com_k < 3:
                    com_k += 1
                    if com_k == 1:
                        com_results_bf_ktrans, com_CounterExamples_bf_ktrans = self.run_verification(full_filepath, combine_invariant)
                        com_results = com_results_bf_ktrans
                        com_CounterExamples = com_CounterExamples_bf_ktrans
                    else:
                        remove_invariant_lines(full_filepath)
                        if not conj_or_lex:
                            k_Transformer.GenerateConcreteBplFile(com_k)
                        else:
                            k_Transformer.GenerateConcreteBplFileLexical(com_k, itVars)
                        com_results, com_CounterExamples = self.run_verification(k_file_name, combine_invariant)
                    if com_k == 1:
                        com_results_bf_ktrans = com_results
                        com_CounterExamples_bf_ktrans = com_CounterExamples
                    self.invariant_verified_freq += 1
                    if com_results[0] == RESULT_VERIFIED:
                        result = RESULT_VERIFIED
                        invariant = combine_invariant
                        k = com_k
                        invariant_end_time = time.perf_counter()
                        current_invariant_time = invariant_end_time - invariant_start_time
                        break
                    if com_results[0] == RESULT_ERROR:
                        result = RESULT_ERROR
                        break
                    if com_results[0] == RESULT_INV_ERROR:
                        result = RESULT_INV_ERROR
                        break
                if len(com_results_bf_ktrans) == 1:
                    com_result = com_results_bf_ktrans[0]
                    if com_result == RESULT_VERIFIED:
                        invariant_end_time = time.perf_counter()
                        current_invariant_time = invariant_end_time - invariant_start_time
                        break
                    if com_result == RESULT_TIMEOUT:
                        print("Timeout when verifying file: {} with invariant: {}".format(full_filepath, combine_invariant))
                        invariant_end_time = time.perf_counter()
                        current_invariant_time = invariant_end_time - invariant_start_time
                        if current_invariant_time > time_limit:
                            break
                    if com_result == RESULT_ERROR:
                        print("Error when verifying file: {} with loop_bound: {}".format(full_filepath, loop_bound))
                        invariant_end_time = time.perf_counter()
                        current_invariant_time = invariant_end_time - invariant_start_time
                        break
                    if com_result == RESULT_INV_ERROR:
                        print("Error when verifying file: {} with invariant: {}".format(full_filepath, combine_invariant))
                        invariant_end_time = time.perf_counter()
                        current_invariant_time = invariant_end_time - invariant_start_time
                        continue
                    if com_result == RESULT_ASSERT_FAILED_HOLD:
                        print("Assertion failed to hold when verifying file: {} with invariant: {}".format(full_filepath, combine_invariant))
                        smt_file = full_filepath[0: -4] + '.smt'
                        rechecker = ReInvariantChecker('/tmpfs/tmp', full_filepath, smt_file, 'i', conj_or_lex, self.boogie_dir, invariant, loop_bound, com_k, log_file = './logs/rechecker_logs/new_extract_ce_noind.log')
                        max_bound = 30
                        error_from_loopbound = rechecker.run_analysis(com_CounterExamples_bf_ktrans[0], max_bound=max_bound, conj_or_lexical=conj_or_lex)
                        if error_from_loopbound == 2:
                            print(f"Program verified by CBC within loop bound {max_bound}, terminating within {max_bound} iterations.")
                            invariant_end_time = time.perf_counter()
                            current_invariant_time = invariant_end_time - invariant_start_time
                            result = RESULT_VERIFIED
                            invariant = "CBC Bound-- " + str(max_bound)
                            break
                        elif isinstance(error_from_loopbound, tuple) and error_from_loopbound[0] == 1:
                            print("This failure is caused by the loop bound")
                            invariant_end_time = time.perf_counter()
                            invariant = combine_invariant
                            current_invariant_time = invariant_end_time - invariant_start_time
                            result = RESULT_ASSERT_FAILED_HOLD
                            # Use the real counterexample state (variable assignments from assume statements)
                            CE = error_from_loopbound[1]
                            break
                        elif error_from_loopbound == 1:
                            # Compatible with old version return format
                            print("This failure is caused by the loop bound")
                            invariant_end_time = time.perf_counter()
                            invariant = combine_invariant
                            current_invariant_time = invariant_end_time - invariant_start_time
                            result = RESULT_ASSERT_FAILED_HOLD
                            CE = com_CounterExamples_bf_ktrans[0]
                            break
                        remove_invariant_lines(full_filepath)
            invariant_end_time = time.perf_counter()
            current_invariant_time = invariant_end_time - invariant_start_time
        if (current_invariant_time > time_limit or retry_count > 3) and result != RESULT_VERIFIED and result != RESULT_ASSERT_FAILED_HOLD and result != RESULT_ERROR:
            result = RESULT_TIMEOUT
        CE = None
        self.invariant_time += current_invariant_time
        return result, invariant, k, CE

    def run_verification(self, k_file_name, invariant):
        # 1-verified 2-failed 3-timeout 4-error
        """Run the Boogie verification process"""
        self.stdout_lines = []
        remove_invariant_lines(k_file_name)
        insert_invariant(invariant, k_file_name)
        verified_start_time = time.perf_counter()
        command = self.setup_command(k_file_name)
        # Change to Boogie directory and run process
        current_dir = os.path.abspath('.')
        process = None
        os.chdir(self.boogie_dir)
        Timer = [self.timeoutMonitor, '--foreground', '--kill-after', '1', str(int(self.verified_timeout) + 1)]
        try:
            process = subprocess.Popen(
                Timer + command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                start_new_session=True
            )
        finally:
            os.chdir(current_dir)
        
        # Process output
        try:
            self._process_output(process, verified_start_time)
            process.wait()
            if process.returncode in (124, 137):  # timeoutMonitor exit code
                self._terminate_process_tree(process)
                return [RESULT_TIMEOUT], []
            verified_end_time = time.perf_counter()
            self.invariant_verified_time = self.invariant_verified_time + verified_end_time - verified_start_time
            # Analyze results
        except VerificationTimeoutError:
            self._terminate_process_tree(process)
            return [RESULT_TIMEOUT], []
        try:
            rets, CounterExamples = self._analyze_results()
        except RuntimeError as e:
            print(f"Error during analysis: {e}")
            return [RESULT_INV_ERROR], []
        finally:
            if process:
                if process.stdout:
                    process.stdout.close()
                if process.stderr:
                    process.stderr.close()
        return rets, CounterExamples

    def _terminate_process_tree(self, process):
        """Terminate the timeout wrapper and any spawned children."""
        if not process:
            return
        if process.poll() is not None:
            return
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
        except OSError:
            return
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            process.wait()

    def _process_output(self, process, verified_start_time):
        """Process the output from Boogie execution"""
        while process.poll() is None:
            cur_time = time.perf_counter()
            if cur_time - verified_start_time > self.verified_timeout:
                self._terminate_process_tree(process)
                raise VerificationTimeoutError()
            line = process.stdout.readline().decode().strip()
            if line.startswith('\n') or line == '':
                continue
                
            self.stdout_lines.append(line)

    def _analyze_results(self):
        """Analyze the verification results"""
        if not self.stdout_lines:
            raise RuntimeError('No output from Boogie execution')
            
        result_line = self.stdout_lines[-1]
        #inv_line = self.stdout_lines[-4] if len(self.stdout_lines) >= 4 else None
        
        print(result_line)
        
        # Try first pattern
        re_matcher = r'Boogie program verifier finished with (\d+) verified, (\d+) error(s)?'
        re_result = re.search(re_matcher, result_line)
            
        if not self.stdout_lines:
            raise RuntimeError('No output from Boogie execution')
            
        result_line = self.stdout_lines[-1]
        
        if re_result:
            verified_num = int(re_result.group(1))
            error_num = int(re_result.group(2))
            
            # Case 1: Verification succeeded
            if verified_num != 0 and error_num == 0:
                return [RESULT_VERIFIED], []
            
            results = parse_boogie_errors(self.stdout_lines, error_num)
            CEs = extract_all_CEmodels(self.stdout_lines)
            if results and CEs and len(results) == len(CEs):
                return results, CEs
            else:
                raise RuntimeError('Mismatch in number of errors and counterexamples extracted')
        error_match = "errors detected in.*"
        re_error = re.search(error_match, result_line)
        if re_error:
            error_line = self.stdout_lines[-2]
            # Extract file path and line number from error_line
            # Example: '/tmpfs/tmp/K_nonlin_jump_over_1_term.bpl(7,53): error: ")" expected'
            error_pattern = r"^(.+\.bpl)\((\d+),\d+\):"
            match = re.match(error_pattern, error_line)
            if match:
                bpl_file_path = match.group(1)
                error_line_num = int(match.group(2))
                try:
                    # Read the error line
                    with open(bpl_file_path, 'r') as f:
                        lines = f.readlines()
                        if 0 < error_line_num <= len(lines):
                            error_code_line = lines[error_line_num - 1].strip()
                            # Check if it starts with assume
                            if error_code_line.startswith('assume'):
                                return [RESULT_ERROR], []
                            else:
                                return [RESULT_INV_ERROR], []
                except (IOError, OSError) as e:
                    print(f"Failed to read file {bpl_file_path}: {e}")
            
            if results and CEs and len(results) == len(CEs):
                return results, CEs
            else:
                raise RuntimeError('Mismatch in number of errors and counterexamples extracted')
        # --- Other cases ---           
        # Case 4: Other unrecognized errors (e.g., ICE Runtime Error)
        print('Unrecognized Boogie output format. Treating as general error.')
        print(reduce(lambda x, y: f'{x}\n{y}', self.stdout_lines))
        return [RESULT_INV_ERROR], []

    def get_output_lines(self):
        """Get all output lines"""
        return self.stdout_lines
    
    def BMC_and(self, bmc_Transformer, invariant, lexical):
        k = 10
        bmc_file_name = bmc_Transformer.CBCfileName
        bmc_file = bmc_file_name[0: -4] + "_bmc.bpl"
        results = []
        #while k <= 10 and not (result == RESULT_VERIFIED or result == RESULT_ERROR):
        bmc_Transformer.GenerateConcreteBplFile(k, True, lexical)
        remove_assert_lines(bmc_file_name, bmc_file)
        #insert_invariant(invariant, bmc_file_name)
        insert_assert_invariant(invariant, bmc_file, lexical)
        results, CEs = self.run_verification(bmc_file, invariant)
        if results[0] == RESULT_VERIFIED:
            return True
        else:
            return False

    def BMC_or(self, bmc_Transformer, invariant, lexical):
        k = 10
        bmc_file_name = bmc_Transformer.CBCfileName
        bmc_file = bmc_file_name[0: -4] + "_bmc.bpl"
        results = []
        #while k <= 10 and not (result == RESULT_VERIFIED or result == RESULT_ERROR):
        bmc_Transformer.GenerateConcreteBplFile(k, True, lexical)
        remove_assert_lines(bmc_file_name, bmc_file)
        #insert_invariant(invariant, bmc_file_name)
        insert_assert_invariant(invariant, bmc_file, lexical)
        results, CEs = self.run_verification(bmc_file, invariant)
        if results[0] == RESULT_VERIFIED or results[0] == RESULT_TIMEOUT:
            return False
        else:
            return True

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

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Loop bound verification with invariant inference')
    parser.add_argument('--config', '-c', type=str, default='config.yaml',
                        help='Path to configuration file (default: config.yaml)')
    parser.add_argument('--llm-type-lb', type=int, default=None,
                        help='LLM type for loop bound (overrides config)')
    parser.add_argument('--llm-type-inv', type=int, default=None,
                        help='LLM type for invariant (overrides config)')
    parser.add_argument('--log-filename', type=str, default=None,
                        help='Log filename (overrides config)')
    args = parser.parse_args()
    
    # Load configuration from YAML file
    config = load_config(args.config)
    
    # Apply command line overrides
    if args.llm_type_lb is not None:
        config['llm_lb']['type'] = args.llm_type_lb
    if args.llm_type_inv is not None:
        config['llm_invariant']['type'] = args.llm_type_inv
    if args.log_filename:
        config['logging']['log_filename'] = args.log_filename
    
    # Extract configuration values
    tmpDir = config['directories']['tmp_dir']
    inputdir = config['directories']['input_dir']
    input_lexdir = config['directories']['input_lex_dir']
    llm_type_loop_bound = config['llm_lb']['type']
    llm_type = config['llm_invariant']['type']
    out_filename = config['output']['result_filename']
    log_dir = config['logging']['log_dir']
    log_filename = config['logging']['log_filename']
    
    # Extract verification parameters from config
    max_conj_iterations = config['verification'].get('max_conj_iterations', 5)
    max_lex_iterations = config['verification'].get('max_lex_iterations', 15)
    
    # Get file list from config (generated by run_batch_verification.py)
    file_list = config.get('file_list', [])
    
    # Print configuration
    print("=" * 60)
    print("Configuration:")
    print(f"  Loop Bound LLM Type: {llm_type_loop_bound}")
    print(f"  Invariant LLM Type: {llm_type}")
    print(f"  Input Dir: {inputdir}")
    print(f"  Log Dir: {log_dir}")
    print(f"  Log File: {log_filename}")
    print(f"  Output File: {out_filename}")
    if file_list:
        print(f"  File List: {len(file_list)} files to process")
    else:
        print(f"  File List: (empty - will process all files)")
    print(f"  Max Conjunctive Iterations: {max_conj_iterations}")
    print(f"  Max Lexicographic Iterations: {max_lex_iterations}")
    print("=" * 60)
    
    success_count = 0
    failure_count = 0
    time_out_count = 0
    error_count = 0
    result = []
    
    logger = setup_logging(log_dir, log_filename)
    
    # Determine files to process
    if file_list:
        # Process files from the config file_list
        # Build full paths from filenames
        files_to_process = []
        for filename in file_list:
            # Find the full path for this filename
            full_path = os.path.join(inputdir, filename, filename + ".bpl")
            if os.path.exists(full_path):
                files_to_process.append((filename, full_path))
            else:
                print(f"Warning: File not found: {full_path}")
        print(f"Processing {len(files_to_process)} files from file_list")
    else:
        # Process all files in input directory
        boogie_files = find_bpl_files(inputdir)
        files_to_process = []
        for inputfile in boogie_files:
            last_slash_index = inputfile.rfind('/')
            filename = inputfile[last_slash_index + 1: -4]
            files_to_process.append((filename, inputfile))
        print(f"Processing all {len(files_to_process)} files from input directory")
    
    for filename, inputfile in files_to_process:
        full_filename = filename + ".bpl"
        origin_file = inputdir + "/" + filename + "/" + full_filename
        
        if match_log_string(log_dir, filename, log_filename):
            print(f"Skipping {filename} as it has already been processed")
            continue
        iter_back = 0
        prompt_type = 0
        feed_back_message =""
        itvar = 'i'
        boogie_code = read_file_to_string(inputfile)
        c_code = read_file_to_string_c(filename)
        verification_ret = 0
        conj_or_lex = False
        previous_loop_bound = []
        previous_llm_answer = []
        repeat_count = 0
        repeat_notice = False
        CE = None
        # Maximum max_conj_iterations iterations, exit on successful verification
        while(iter_back < max_conj_iterations and verification_ret != 1):
            #llm_answer = openai_gen_answer(llm_type, boogie_code, prompt_type, feed_back_message)
            if previous_llm_answer:
                if not repeat_notice:
                    feed_back_message = previous_llm_answer[-1][0]
                    prompt_type = previous_llm_answer[-1][1]
                    CE = previous_llm_answer[-1][2]
                else:
                    all_history_tmp = list(zip(*previous_llm_answer))
                    all_history = [list(item) for item in all_history_tmp]
                    feed_back_message, prompt_type, CE = all_history
            (llm_answer, loop_bound_infer_time) = openai_gen_answer(0, llm_type_loop_bound, boogie_code, conj_or_lex, prompt_type, feed_back_message, CE, repeat_notice)
            #llm_answer = 'assume(i >= y); assume(i >= z);'
            llm_answer_raw = remove_empty(llm_answer)
            #feed_back_message[0] = llm_answer
            loop_bound, llm_answer = extract_assume_expressions(llm_answer_raw)
            if loop_bound in previous_loop_bound:
                print(f"Loop bound {llm_answer} has already been tried.")
                logger.info(f"Loop bound {llm_answer} has already been tried.")
                repeat_count += 1
                iter_back += 1
                if repeat_count >= 1:
                    repeat_notice = True
                continue
            # If the right side contains a counter, skip to the next generation iteration
            repeat_notice = False
            i_break_flag = False
            for bound in loop_bound:
                pattern = r'\bi\b'
                if re.search(pattern, bound[1]):
                    i_break_flag = True
                    break
            if i_break_flag:
                prompt_type = 1
                logger.info(f"Counter error with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                iter_back += 1
                previous_llm_answer.append([str(llm_answer), prompt_type])
                continue
            previous_loop_bound.append(loop_bound)
            k_Transformer = K_Transformer(tmpDir, origin_file, itvar)
            # Create a new BoogieVerifier object for each loop bound generation to track timing data separately
            verifier = BoogieVerifier(k_Transformer.fileName, origin_file, learner='dt_penalty')
            verifier.GenerateConcreteBplFile(loop_bound)
            if len(loop_bound) == 1:
                simple_bound = loop_bound[0][1]
                if BoogieVerifier.IsNumber(simple_bound):
                    simple_bound = int(simple_bound)
                    if simple_bound < 100000:  # CBC unrolling should not be too large
                        cbcchecker = CBChecker(tmpDir, k_Transformer.fileName, itvar)
                        cbc_ret = cbcchecker.ExecuteCBC(simple_bound, timeout=60, timeoutMonitor='/usr/bin/timeout')
                        if cbc_ret == 1:
                            print(f"Verification succeeded with the loop bound: {llm_answer}, invariant: CBC Bound-- {simple_bound}")
                            logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, invariant: CBC Bound-- {simple_bound}, k: 0, invariant: None, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                            success_count += 1
                            verification_ret = 1
                            break
                        elif cbc_ret == 2:
                            print("CBC verification failed")
                            logger.info(f"CBC verification failed with the loop bound: {llm_answer}, file: {full_filename} , k: 0, feed_back_iter: {iter_back}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}")
                            simple_bound = simple_bound + 3 # try const added
                            cbc_ret = cbcchecker.ExecuteCBC(simple_bound, timeout=60, timeoutMonitor='/usr/bin/timeout')
                            if cbc_ret == 1:
                                print(f"Verification succeeded with the loop bound: {llm_answer}, invariant: CBC Bound-- {simple_bound}")
                                logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, invariant: CBC Bound-- {simple_bound}, k: 0, invariant: None, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                                success_count += 1
                                verification_ret = 1
                                break
                            elif cbc_ret == 2:
                                print("CBC verification failed after adding const")
                                logger.info(f"CBC verification failed after adding const with the loop bound: {llm_answer}, file: {full_filename} , k: 0, feed_back_iter: {iter_back}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}")
                                prompt_type = 2
                                previous_llm_answer.append([str(llm_answer), prompt_type])
                                iter_back += 1
                                continue
                        prompt_type = 3
                        previous_llm_answer.append([llm_answer, prompt_type, None])
                        iter_back += 1
                        continue
            try:
                #verification_ret, invariant = verifier.run_verification(k_Transformer.K_fileName)
                verification_ret, invariant, k, CE = verifier.invariant_infer(full_filename, llm_answer, conj_or_lex, prompt_type, llm_type=llm_type)
                assert verification_ret != RESULT_INV_FAILED_HOLD and verification_ret != RESULT_INV_FAILED_MAINTAIN, "Invariant inference failure should not be returned"
                if verification_ret == RESULT_VERIFIED:
                    print(f"Verification succeeded with the loop bound: {llm_answer}, invariant: {invariant}")
                    logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, invariant: {invariant}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                    success_count += 1
                    break
                elif verification_ret == RESULT_ASSERT_FAILED_HOLD:
                    print("Verification failed")
                    logger.info(f"Verification failed with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, feed_back_iter: {iter_back}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}")
                    prompt_type = 2
                    previous_llm_answer.append([llm_answer, prompt_type, CE])
                elif verification_ret == RESULT_TIMEOUT:
                    print("Verification timed out")
                    logger.info(f"Verification timed out with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, feed_back_iter: {iter_back}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}")
                    prompt_type = 3
                    previous_llm_answer.append([llm_answer, prompt_type, None])
                elif verification_ret == RESULT_ERROR:
                    print("ICE Runtime error")
                    logger.info(f"ICE Runtime error with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                    prompt_type = 1
                    previous_llm_answer.append([llm_answer, prompt_type, None])
                    continue
            except RuntimeError as e:
                print(f"Error during verification: {e}")
            new_loop_bound = []
            for bound in loop_bound:
                new_bound = (bound[0], bound[1] + '+3')
                new_loop_bound.append(new_bound)
            verifier.GenerateConcreteBplFile(new_loop_bound)
            k_Transformer.GenerateConcreteBplFile(1)
            #verification_ret, invariant = verifier.run_verification(k_Transformer.K_fileName)
            const_add_ret, const_add_invariant, const_add_k, _ = verifier.invariant_infer(full_filename, llm_answer, conj_or_lex, prompt_type, llm_type=llm_type)
            if const_add_ret == 1:
                verification_ret = const_add_ret
                invariant = const_add_invariant
                k = const_add_k
                print(f"Verification succeeded with the loop bound: {llm_answer}, const_part: 3, invariant: {invariant}")
                logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, const_part: 3, invariant: {invariant}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                success_count += 1
            iter_back += 1


        previous_lexical_loop_bound = []
        prompt_type = 0
        repeat_notice = False
        CE = None
        while(verification_ret != 1 and iter_back < max_lex_iterations):
            k = 1
            repeat_count = 0
            conj_or_lex = True
            origin_file = input_lexdir + "/" + filename + "/" + full_filename
            if previous_llm_answer:
                if not repeat_notice:
                    feed_back_message = previous_llm_answer[-1][0]
                    prompt_type = previous_llm_answer[-1][1]
                    CE = previous_llm_answer[-1][2]
                else:
                    all_history_tmp = list(zip(*previous_llm_answer))
                    all_history = [list(item) for item in all_history_tmp]
                    feed_back_message, prompt_type, CE = all_history
            #llm_answer = openai_gen_answer(llm_type, boogie_code, prompt_type, feed_back_message)
            (llm_answer, loop_bound_infer_time) = openai_gen_answer(0, llm_type_loop_bound, c_code, conj_or_lex, prompt_type, feed_back_message, CE, repeat_notice)
            #llm_answer = "assume(i0 >= maxId - id && i1 >= maxId + 1);"
            llm_answer_raw = remove_empty(llm_answer)
            #feed_back_message[0] = llm_answer
            lexical_loop_bound, llm_answer = extract_lexical_bounds(llm_answer_raw)
            if lexical_loop_bound in previous_lexical_loop_bound:
                print(f"Lexical loop bound {llm_answer} has already been tried.")
                logger.info(f"Lexical loop bound {llm_answer} has already been tried.")
                iter_back += 1
                repeat_count += 1
                if repeat_count >= 1:
                    repeat_notice = True
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
                logger.info(f"Counter error with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                iter_back += 1       
                continue
            previous_lexical_loop_bound.append(lexical_loop_bound)
            k_Transformer = K_Transformer(tmpDir, origin_file, itvar)
            verifier = BoogieVerifier(k_Transformer.fileName, origin_file, learner='dt_penalty')
            itVars = lex_counter_distill(lexical_loop_bound, itvar)
            if not itVars:
                print(f"Error during lexicographic loop bound format with this answer: {llm_answer}")
                logger.info(f"Error during lexicographic loop bound format with this answer: {llm_answer}, file: {full_filename}, loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                prompt_type = 1
                iter_back += 1
                continue
            try:
                verifier.GenerateConcreteBplFileLexicalTemplate(lexical_loop_bound)
            except IndexError as e:
                print(f"Error during klexical template generation: {e}")
                logger.info(f"Klexical template generation error with the loop bound: {llm_answer}, file: {full_filename}, loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                prompt_type = 1
                iter_back += 1 
                continue
            #k_Transformer.GenerateConcreteBplFileLexical(1)
            const_part = 0
            '''try:
                k_Transformer.GenerateConcreteBplFileLexical(k, itVars)
            except RuntimeError as e:
                print(f"Error during k-transformer: {e}")
                logger.info(f"K-transformer error with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                break
            except IndexError as e:
                print(f"Error during k-transformer: {e}")
                logger.info(f"K-transformer error with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                break'''
            try:
                #verification_ret, invariant = verifier.run_verification(k_Transformer.K_fileName)
                verification_ret, invariant, k, CE = verifier.invariant_infer(full_filename, llm_answer, conj_or_lex, prompt_type, itVars=itVars, llm_type=llm_type)
                assert verification_ret != RESULT_INV_FAILED_HOLD and verification_ret != RESULT_INV_FAILED_MAINTAIN, "Invariant inference failure should not be returned"
                if verification_ret == RESULT_VERIFIED:
                    print(f"Verification succeeded with the loop bound: {llm_answer}, invariant: {invariant}")
                    logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, invariant: {invariant}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                    success_count += 1
                    break
                elif verification_ret == RESULT_ASSERT_FAILED_HOLD:
                    print("Verification failed")
                    logger.info(f"Verification failed with the loop bound: {llm_answer}, file: {full_filename} , k: {k}, feed_back_iter: {iter_back}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}")
                    prompt_type = 2
                    previous_llm_answer.append([llm_answer, prompt_type, CE])
                elif verification_ret == RESULT_TIMEOUT:
                    print("Verification timed out")
                    logger.info(f"Verification timed out with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, feed_back_iter: {iter_back}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}")
                    prompt_type = 3
                    previous_llm_answer.append([llm_answer, prompt_type, None])
                elif verification_ret == RESULT_ERROR:
                    print("ICE Runtime error")
                    logger.info(f"ICE Runtime error with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                    prompt_type = 1
                    previous_llm_answer.append([llm_answer, prompt_type, None])
                    break
            except RuntimeError as e:
                print(f"Error during verification: {e}")
            new_lexi_loop_bound = []
            for counter in lexical_loop_bound:
                new_lexi_counter = []
                for bound in counter:
                    bound = bound + '+3'
                    new_lexi_counter.append(bound)
                new_lexi_loop_bound.append(new_lexi_counter)
            verifier.GenerateConcreteBplFileLexicalTemplate(new_lexi_loop_bound)
            k_Transformer.GenerateConcreteBplFileLexical(1, itVars)
            #verification_ret, invariant = verifier.run_verification(k_Transformer.K_fileName)
            const_add_ret, const_add_invariant, const_add_k, _ = verifier.invariant_infer(full_filename, llm_answer, conj_or_lex, prompt_type, itVars=itVars, llm_type=llm_type)
            if const_add_ret == 1:
                verification_ret = const_add_ret
                invariant = const_add_invariant
                k = const_add_k
                print(f"Verification succeeded with the loop bound: {llm_answer}, const_part: 3, invariant: {invariant}")
                logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: {k}, const_part: 3, invariant: {invariant}, verification_time: {verifier.invariant_time}, veri_details: [{verifier.invariant_infer_time}, {verifier.invariant_infer_freq}, {verifier.invariant_verified_time}, {verifier.invariant_verified_freq}, {verifier.com_invariant_verified_freq}], loop_bound_infer_time: {loop_bound_infer_time}, feed_back_iter: {iter_back}")
                success_count += 1
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

