import re
import subprocess
import os
import time
from CBC_Transform import CBChecker
from utils import *
from extract_loophead_variables_final import extract_loophead_variables

RESULT_TIMEOUT = 0
RESULT_VERIFIED = 1
RESULT_ERROR = 2
RESULT_INV_FAILED_HOLD = 3
RESULT_INV_FAILED_MAINTAIN = 4
RESULT_ASSERT_FAILED_HOLD = 5

class ReInvariantChecker:
    """
    A class for analyzing Boogie output, generating state assumptions, and iteratively checking loop invariants.
    
    This class encapsulates the following workflow:
    1. Parse the model generated after Boogie verification failure.
    2. Extract key pre-loop state from the model according to specific rules.
    3. Insert this state as an assume statement into a bounded Boogie program copy.
    4. Iteratively call Boogie to verify the copy, to determine if failure is caused by loop bound or invariant itself.
    """

    def __init__(self, working_dir: str, boogie_file: str, smt_file: str = None, counter_var_name: str = 'i', conj_or_lex = False, boogie_exe_path: str = './ice/popl16_artifact/Boogie/Binaries', invariant: str = None, loop_bound = None, k: int = None, log_file: str = 'logs/reinvariant_checker_noind.log'):
        """
        Initialize ReInvariantChecker.

        Args:
            working_dir (str): Temporary working directory for generated files.
            boogie_file (str): Path to the original Boogie (.bpl) file.
            smt_file (str): Path to corresponding SMT file for extracting LoopHead variables. If None, uses traditional method.
            counter_var_name (str): Variable name used as loop counter in Boogie code.
            boogie_exe_path (str): Relative or absolute path to directory containing Boogie.exe.
        """
        if not os.path.exists(boogie_file):
            raise FileNotFoundError(f"Specified Boogie file does not exist: {boogie_file}")
            
        self.working_dir = working_dir
        self.boogie_file = boogie_file
        self.smt_file = smt_file
        self.counter_var_name = counter_var_name
        self.boogie_exe_dir = os.path.abspath(boogie_exe_path)
        self.cb_checker = CBChecker(self.working_dir, self.boogie_file, self.counter_var_name)
        self.invariant = invariant
        self.loop_bound = loop_bound
        self.k_value = k
        self.log_file = log_file
        try:
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        except Exception:
            pass
        self._log_construct()
        
        # If SMT file is provided, extract LoopHead variables
        self.loophead_variables = set()
        if smt_file and os.path.exists(smt_file):
            try:
                self.loophead_variables = extract_loophead_variables(smt_file, conj_or_lex)
                print(f"Extracted LoopHead variables from SMT file: {', '.join(sorted(self.loophead_variables))}")
            except Exception as e:
                print(f"Warning: Unable to extract variables from SMT file: {e}")
                self.loophead_variables = set()

    def _analyze_model(self, model_lines):
        """
        Parse model lines, extract variable assignments, base variable names and SSA mapping.
        (Provided by user and slightly modified to return values)
        """
        modelDict = {}
        recordVars = set()
        
        for line in model_lines:
            rexpr = r'(.*)? -> \(?(- )?(\d+)\)?'
            reM = re.search(rexpr, line)

            if reM is None:
                continue
            
            varName = reM.group(1).strip()
            if varName.startswith(r'%lbl%') or not varName:
                continue
                
            if '@' in varName:
                realName = varName[:varName.find('@')]
                recordVars.add(realName)
            else:
                recordVars.add(varName)

            valueV = int(reM.group(3))
            if reM.group(2) is not None:
                valueV = -valueV
            modelDict[varName] = valueV

        return modelDict, recordVars
    
    def _map_smt_to_boogie_variables(self, smt_variables: set, model_dict: dict) -> dict:
        """
        Map variables from SMT file to corresponding variables in Boogie model.
        
        Args:
            smt_variables: Set of variables extracted from SMT file
            model_dict: Boogie model dictionary
            
        Returns:
            Mapped variable dictionary {base_var_name: value}
        """
        mapped_vars = {}
        for smt_var in smt_variables:
            if '@' in smt_var:
                # Handle variables with SSA version, e.g., i@0, x@1
                base_var = smt_var.split('@')[0]
                if smt_var in model_dict:
                    mapped_vars[base_var] = model_dict[smt_var]
                    print(f"  - Mapped: {base_var} = {model_dict[smt_var]} (from SMT variable {smt_var})")
                else:
                    print(f"  - Warning: SMT variable {smt_var} not found in Boogie model")
            else:
                # Handle variables without SSA version
                if smt_var in model_dict:
                    mapped_vars[smt_var] = model_dict[smt_var]
                    print(f"  - Mapped: {smt_var} = {model_dict[smt_var]}")
                else:
                    print(f"  - Warning: Variable {smt_var} not found in Boogie model")
        
        return mapped_vars

    def _extract_key_state_dynamically(self, model_dict: dict, record_vars: set):
        """
        Extract key state from model based on LoopHead_correct scope variables in SMT file, and generate assume statement.
        If SMT file is available, use variables extracted from it; otherwise use traditional method.
        """
        key_state = {}
        
        if self.loophead_variables:
            # Use LoopHead variables extracted from SMT file
            print(f"Using LoopHead variables from SMT file: {', '.join(sorted(self.loophead_variables))}")
            key_state = self._map_smt_to_boogie_variables(self.loophead_variables, model_dict)
        else:
            # Fall back to traditional method
            print("SMT file not provided or extraction failed, using traditional method to extract variables")
            
            # 1. Handle loop counter variable, must be @0
            counter_ssa_name = f"{self.counter_var_name}@0"
            if counter_ssa_name in model_dict:
                key_state[self.counter_var_name] = model_dict[counter_ssa_name]
            else:
                print(f"Warning: Key variable {counter_ssa_name} not found in model. Cannot determine pre-loop state.")
                return None

            # 2. Handle all other variables
            for var in record_vars:
                if var == self.counter_var_name:
                    continue

                ssa_v1 = f"{var}@1"
                ssa_v0 = f"{var}@0"
                
                if ssa_v1 in model_dict:
                    key_state[var] = model_dict[ssa_v1]
                elif ssa_v0 in model_dict:
                    key_state[var] = model_dict[ssa_v0]
                elif var in model_dict: # Handle global or input variables (no @ suffix)
                    key_state[var] = model_dict[var]
                else:
                    print(f"Info: Variable '{var}' has no @0 or @1 assignment in model, will not be included in state assumption.")

        if not key_state:
            print("Failed to extract any key state variables")
            return None

        state_conditions = [f"{var} == {val}" for var, val in key_state.items()]
        assume_statement = f"assume {' && '.join(state_conditions)};"
        
        print(f"Generated assume statement: {assume_statement}")
        return assume_statement

    def _log_line(self, msg: str):
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(msg + "\n")
        except Exception:
            pass

    def _log_construct(self):
        ts = time.strftime('%Y-%m-%d %H:%M:%S')
        inv = (self.invariant or '').replace('\n', ' ')
        lb = str(self.loop_bound) if self.loop_bound is not None else ''
        kv = str(self.k_value) if self.k_value is not None else ''
        bf = self.boogie_file
        self._log_line(f"{ts} | construct ReInvariantChecker | file: {bf} | k: {kv} | loop_bound: {lb} | invariant: {inv}")

    def _insert_before_last_assert(self, filepath: str, string_to_insert: str):
        """
        Read file, find the last line starting with 'assert', and insert specified string before it.
        File will be modified in place.
        """
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            return

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error: Failed to read file {filepath}: {e}")
            return

        assert_pattern = re.compile(r'^\s*assert', re.IGNORECASE)
        target_index = -1
        for i in range(len(lines) - 1, -1, -1):
            if assert_pattern.match(lines[i]):
                target_index = i
                break
                
        if target_index != -1:
            if not string_to_insert.endswith('\n'):
                string_to_insert += '\n'
            lines.insert(target_index, string_to_insert)
            
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                #print(f"Successfully inserted statement before line {target_index} in {filepath}.")
                #print(f"Inserted content: {string_to_insert.strip()}")
            except Exception as e:
                print(f"Error: Failed to write file {filepath}: {e}")
        else:
            print(f"Warning: No assert statement found in {filepath}, file not modified.")
            
    def _run_boogie(self, filepath: str, timeout_seconds: int = 60) -> str:
        """
        Execute verification on specified Boogie file.
        """
        boogie_args = [
            '/noinfer', 
            '/contractInfer',
            '/printAssignment', 
            '/printModel:4',
            '/trace'
        ]
        command = ['mono', 'Boogie.exe'] + boogie_args + [filepath]
        
        original_dir = os.getcwd()
        try:
            os.chdir(self.boogie_exe_dir)
            timer_command = ['/usr/bin/timeout', '--foreground', '--kill-after', '1', str(timeout_seconds)]
            process = subprocess.Popen(
                timer_command + command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True # Use text=True to get string output
            )
            stdout, stderr = process.communicate()
            return stdout
        finally:
            os.chdir(original_dir) # Ensure returning to original directory regardless of success or failure

    def run_analysis(self, model_output: str, max_bound: int = 10, conj_or_lexical: bool = False):
        remove_invariant_lines(self.boogie_file)
        
        model_lines = model_output.split('\n')
        try:
            model_dict, record_vars = self._analyze_model(model_lines)
        except Exception as e:
            print(f"Model Analysis Failed: {e}")
            return 0

        # Step 3: Extract key state and generate assume statement
        #print("\n>>> Step 3: Extracting key state...")
        state_assumption = self._extract_key_state_dynamically(model_dict, record_vars)
        if not state_assumption:
            print("Abort without Extraction")
            return 0
        print(f"  - Extracred assume statement: {state_assumption}")

        
        # First use CBC to check if program terminates within max_bound
        cbc_result = self.cb_checker.ExecuteCBC(max_bound, ret='default', timeout=20, timeoutMonitor='/usr/bin/timeout', withloopbound=True, lexical=conj_or_lexical)
        if cbc_result == 1:
            print(f"\nProgram verified by CBC within loop bound {max_bound}, terminating within {max_bound} iterations.")
            return 2
        # Step 4: Loop checking
        #print("\n>>> Step 4: Starting loop bound checking...")
        for i in range(max_bound):
            print(f"\n--- Unrolling iteration {i} ---")
            
            # Generate concrete bpl file
            self.cb_checker.GenerateConcreteBplFile(i, True, lexical=conj_or_lexical)
            tocheckfile = self.cb_checker.CBCfileName

            # Insert state assumption
            self._insert_before_last_assert(tocheckfile, state_assumption)
            
            # Run Boogie
            stdout = self._run_boogie(tocheckfile, timeout_seconds=20)
            
            # Analyze results
            stdout_lines = stdout.split('\n')
            re_matcher = r'Boogie program verifier finished with (\d+) verified, (\d+) error(s)?'
            
            # Usually result is in second-to-last line
            result_line = next((line for line in reversed(stdout_lines) if "Boogie program verifier finished" in line), None)

            if not result_line:
                print('  - Result: Timeout or Boogie execution failed!')
                print('  - Result: Failed to parse verification result from Boogie output.') 
                break # Continue to next bound value

            re_result = re.search(re_matcher, result_line)
            if re_result:
                verified_num = int(re_result.group(1))
                error_num = int(re_result.group(2))
                
                if verified_num > 0 and error_num == 0:
                    print('[info] CBC verified with bound {}, this failure can be caused by the loop bound or the invariant'.format(i))
                else:
                    print("This failure is caused by the loop bound")
                    # log success before returning (1, state_assumption)
                    # First build an f-string containing newlines
                    log_message = f"{time.strftime('%Y-%m-%d %H:%M:%S')} | success | verified_bound: {i} | file: {self.boogie_file} | k: {self.k_value} | loop_bound: {self.loop_bound} | invariant: {self.invariant or ''}"

                    # Process the entire log message, replace newlines
                    self._log_line(log_message.replace('\n', ' '))
                    # Return real counterexample state (variable assignments from assume statement)
                    return (1, state_assumption)
            else:
                print('  - Result: Failed to parse verification result from Boogie output.')        
        print(f"\nStill unable to judge after trying bounds up to {max_bound}.")
        return 0
