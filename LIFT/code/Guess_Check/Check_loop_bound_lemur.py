import os
import re
import sys
import time
import logging
import subprocess
import yaml
import shutil
from typing import List, Tuple, Dict, Optional
from utils import *
from prompt_gen_newiter import openai_gen_answer, llmtype_message_map
from CBC_Transform import CBChecker

from DataInfo import Task_Info

# Import lexical bound processing functions
from utils import extract_lexical_bounds, lex_counter_distill

# Result codes
RESULT_TIMEOUT = 0
RESULT_VERIFIED = 1
RESULT_ERROR = 2
RESULT_FALSIFIED = 3
RESULT_UNKNOWN = 4


def copy_bpl_without_pattern(source_path: str, dest_path: str, pattern: str = "i%") -> None:
    """
    Copy a Boogie (.bpl) file while removing every line containing the given pattern.
    The source file remains untouched; the filtered content is written to dest_path.

    Args:
        source_path: Path to the original .bpl file.
        dest_path: Destination path for the filtered copy.
        pattern: Substring whose presence in a line causes that line to be skipped.
    """
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(source_path, 'r', encoding='utf-8') as src, \
            open(dest_path, 'w', encoding='utf-8') as dst:
        for line in src:
            if pattern not in line:
                dst.write(line)


class LEMURVerifier:
    """Wrapper for LEMUR invariant generation and verification tool"""
    
    def __init__(self, lemur_base_dir='/root/LIFT/experiment/baseline.scripts/Lemur-program-verification/lemur'):
        self.lemur_base_dir = lemur_base_dir
        self.lemur_src_dir = os.path.join(lemur_base_dir, 'src')
        self.lemur_run_script = os.path.join(lemur_base_dir, 'run.sh')
        self.properties_dir = os.path.join(lemur_base_dir, 'benchmarks/sv_comp/properties')
        self.timeout = 900  # 15 minutes per benchmark
        
        # Ensure LEMUR directories exist
        if not os.path.exists(self.lemur_base_dir):
            raise RuntimeError(f"LEMUR directory not found: {self.lemur_base_dir}")
    
    def create_c_with_loop_bound(self, 
                                  original_c_file: str, 
                                  output_c_file: str, 
                                  loop_bound_assumptions: List[str],
                                  is_lexicographic: bool = False,
                                  lexical_loop_bound: List[List[str]] = None,
                                  itVars: List[str] = None) -> bool:
        """
        Insert loop bound assumptions into C file before the loop.
        For lexicographic bounds, also insert decrement logic inside the loop.
        
        Args:
            original_c_file: Path to original C file
            output_c_file: Path to output C file with assumptions
            loop_bound_assumptions: List of assume statements
            is_lexicographic: Whether this is a lexicographic bound
            lexical_loop_bound: 2D list of lexical bounds (for lexicographic case)
            itVars: List of counter variables (for lexicographic case)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(original_c_file, 'r') as f:
                lines = f.readlines()
            
            # Find the first loop (while/for/do)
            loop_line_idx = -1
            loop_body_start = -1
            loop_body_end = -1
            
            for i, line in enumerate(lines):
                stripped = line.strip()
                if stripped.startswith('while') or stripped.startswith('for') or stripped.startswith('do'):
                    loop_line_idx = i
                    # Find loop body start (opening brace)
                    for j in range(i, len(lines)):
                        if '{' in lines[j]:
                            loop_body_start = j
                            break
                    # Find loop body end (closing brace)
                    if loop_body_start != -1:
                        brace_count = 0
                        for j in range(loop_body_start, len(lines)):
                            brace_count += lines[j].count('{')
                            brace_count -= lines[j].count('}')
                            if brace_count == 0:
                                loop_body_end = j
                                break
                    break
            
            if loop_line_idx == -1:
                print(f"Warning: No loop found in {original_c_file}")
                shutil.copy(original_c_file, output_c_file)
                return True
            
            # Determine indentation
            indent = len(lines[loop_line_idx]) - len(lines[loop_line_idx].lstrip())
            indent_str = ' ' * indent
            
            # Create assumption lines (before loop)
            assumption_lines = []
            for assumption in loop_bound_assumptions:
                match = re.search(r'assume\((.*?)\);?', assumption)
                if match:
                    expr = match.group(1)
                    assumption_lines.append(f"{indent_str}assume({expr});\n")
            
            # For lexicographic bounds, add counter declarations and decrement logic
            if is_lexicographic and lexical_loop_bound and itVars:
                # Add counter variable declarations before loop
                counter_decls = []
                for var in itVars:
                    counter_decls.append(f"{indent_str}int {var};\n")
                
                # Add counter initializations
                counter_inits = []
                for i, var in enumerate(itVars):
                    # Initialize to the first bound expression
                    if lexical_loop_bound[i]:
                        init_expr = lexical_loop_bound[i][0]
                        counter_inits.append(f"{indent_str}{var} = {init_expr};\n")
                
                # Generate decrement logic to insert at end of loop body
                decrement_logic = generate_c_decrement_logic(
                    lexical_loop_bound, itVars, indent + 4
                )
                # Insert assert at the start of the loop body: assert(i0 > 0);
                assert_lines = [f"{indent_str}    assert({itVars[0]} > 0);\n"]

                decrement_lines = [f"{indent_str}    // Lexicographic decrement logic\n"]
                decrement_lines.extend(decrement_logic.split('\n'))
                decrement_lines = [line + '\n' if line and not line.endswith('\n') else line 
                                   for line in decrement_lines if line.strip()]
                
                # Build new file content
                new_lines = (
                    lines[:loop_line_idx] +
                    counter_decls +
                    counter_inits +
                    assumption_lines +
                    lines[loop_line_idx:loop_body_start+1] +
                    assert_lines +
                    lines[loop_body_start+1:loop_body_end] +
                    decrement_lines +
                    lines[loop_body_end:]
                )
            else:
                # Simple conjunctive case: insert assumptions, assert(i > 0) at loop start, and i = i - 1 at loop end
                # Try to infer the counter variable name from the first assumption; default to 'i'
                var_name = 'i'
                for assumption in loop_bound_assumptions:
                    m = re.search(r'assume\(\s*([A-Za-z_][A-Za-z0-9_]*)\b', assumption)
                    if m:
                        var_name = m.group(1)
                        break
                assert_line = [f"{indent_str}    assert({var_name} > 0);\n"]
                dec_lines = [f"{indent_str}    {var_name} = {var_name} - 1;\n"]

                new_lines = (
                    lines[:loop_line_idx] +
                    assumption_lines +
                    lines[loop_line_idx:loop_body_start+1] +
                    assert_line +
                    lines[loop_body_start+1:loop_body_end] +
                    dec_lines +
                    lines[loop_body_end:]
                )
            
            with open(output_c_file, 'w') as f:
                f.writelines(new_lines)
            
            return True
            
        except Exception as e:
            print(f"Error creating C file with loop bound: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def create_yaml_config(self, 
                          c_file_path: str, 
                          yaml_file_path: str,
                          working_dir: str,
                          property_type: str = 'reach',
                          data_model: str = 'ILP32') -> bool:
        """
        Create YAML configuration file for LEMUR.
        
        Args:
            c_file_path: Path to C source file (relative to yaml file)
            yaml_file_path: Path to output YAML file
            working_dir: Working directory where properties folder will be created
            property_type: 'reach' for reachability, 'term' for termination
            data_model: ILP32 or LP64
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get relative path from yaml to c file
            yaml_dir = os.path.dirname(yaml_file_path)
            c_filename = os.path.basename(c_file_path)
            
            # Use relative path to properties folder in working_dir
            # The property file will be created by run_lemur method
            if property_type == 'reach':
                property_file = os.path.join(working_dir, 'properties', 'unreach-call.prp')
                expected_verdict = 'true'  # We expect the program to be correct
            else:  # termination
                property_file = os.path.join(working_dir, 'properties', 'termination.prp')
                expected_verdict = 'true'
            
            config = {
                'format_version': '2.0',
                'input_files': c_filename,
                'options': {
                    'data_model': data_model,
                    'language': 'C'
                },
                'properties': [
                    {
                        'expected_verdict': expected_verdict,
                        'property_file': property_file
                    }
                ]
            }
            
            with open(yaml_file_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False, sort_keys=False)
            
            return True
            
        except Exception as e:
            print(f"Error creating YAML config: {e}")
            return False
    
    def run_lemur(self, 
                  yaml_config_path: str,
                  working_dir: str,
                  model: str = 'xdeepseekv32exp',
                  per_instance_timeout: int = 60,
                  iteration: int = None) -> Tuple[int, Optional[str], float, Optional[str]]:
        """
        Run LEMUR verification.
        
        Args:
            yaml_config_path: Path to YAML configuration file
            working_dir: Working directory for LEMUR output
            model: LLM model to use
            per_instance_timeout: Timeout for each verification query
            
        Returns:
            Tuple of (result_code, message, time_taken, counterexample)
            - counterexample: None if verified/unknown, or string with counterexample info if falsified
        """
        start_time = time.perf_counter()
        
        try:
            tmp_dir = "/tmpfs/tmp"
            # Create properties folder in working_dir and copy unreach-call.prp
            properties_dir = os.path.join(tmp_dir, 'properties')
            os.makedirs(properties_dir, exist_ok=True)
            
            source_prp = '/root/LIFT/experiment/baseline.scripts/Lemur-program-verification/lemur/benchmarks/sv_comp/properties/unreach-call.prp'
            dest_prp = os.path.join(properties_dir, 'unreach-call.prp')
            shutil.copy2(source_prp, dest_prp)
            
            logging.info(f"Created properties directory and copied unreach-call.prp to {properties_dir}")
            
            # Prepare command
            command = [
                self.lemur_run_script,
                yaml_config_path,
                '--learn',
                '-v', 'all',
                '--per-instance-timeout', str(per_instance_timeout),
                '-w', working_dir,
                '--model', model
            ]
            
            # Add iteration parameter if provided
            if iteration is not None:
                command.extend(['--iteration', str(iteration)])
            current_dir = os.path.abspath('.')
            os.chdir(self.lemur_base_dir)
            # Run with timeout
            process = subprocess.Popen(
                ['timeout', str(self.timeout)] + command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            os.chdir(current_dir)
            stdout, stderr = process.communicate()
            
            end_time = time.perf_counter()
            time_taken = end_time - start_time
            tmp_file_prename = os.path.basename(yaml_config_path)[:-4] + "_bounded"
            # Determine the temporary work directory created by LEMUR
            temp_work_dir = os.path.join(working_dir, tmp_file_prename)
            
            # Check timeout
            if process.returncode in (124, 137):
                # Keep temporary directory for inspection - no cleanup on timeout
                logging.info(f"LEMUR verification timed out, results preserved in: {temp_work_dir}")
                return RESULT_TIMEOUT, "LEMUR verification timed out", time_taken, None
            
            # Parse results from stdout (primary method)
            # LEMUR outputs verification results as "Level 0 - Verified/Falsified/Unknown"
            result_from_stdout = None
            attempts_count = 0
            
            # Find the last "Level 0 - " message in stdout
            stdout_lines = stdout.strip().split('\n')
            for line in reversed(stdout_lines):
                # Remove ANSI color codes
                clean_line = re.sub(r'\x1b\[[0-9;]*m', '', line)
                
                if 'Level 0 - ' in clean_line:
                    if 'Verified' in clean_line and 'Verifying' not in clean_line:
                        result_from_stdout = RESULT_VERIFIED
                        break
                    elif 'Falsified' in clean_line:
                        result_from_stdout = RESULT_FALSIFIED
                        break
                    elif 'Unknown' in clean_line:
                        result_from_stdout = RESULT_UNKNOWN
                        break
            
            # Extract counterexample information if falsified
            counterexample = None
            #if result_from_stdout == RESULT_FALSIFIED:
            #    counterexample = self._extract_counterexample(stdout, temp_work_dir)
            
            # Try to extract attempts count from result.txt if it exists
            result_file = os.path.join(temp_work_dir, 'result.txt')
            if os.path.exists(result_file):
                try:
                    with open(result_file, 'r') as f:
                        result_content = f.read().strip()
                    
                    if result_content.startswith('verified'):
                        parts = result_content.split(',')
                        attempts_count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                        # Confirm verified status from file
                        if result_from_stdout is None:
                            result_from_stdout = RESULT_VERIFIED
                    elif result_content.startswith('falsified'):
                        parts = result_content.split(',')
                        attempts_count = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
                        # Confirm falsified status from file
                        if result_from_stdout is None:
                            result_from_stdout = RESULT_FALSIFIED
                except Exception as e:
                    logging.warning(f"Error reading result.txt: {e}")
            
            # Return based on parsed result
            if result_from_stdout == RESULT_VERIFIED:
                msg = f"Verified with {attempts_count} attempts" if attempts_count > 0 else "Verified"
                result = (RESULT_VERIFIED, msg, time_taken, None)
            elif result_from_stdout == RESULT_FALSIFIED:
                msg = f"Falsified after {attempts_count} attempts" if attempts_count > 0 else "Falsified"
                result = (RESULT_FALSIFIED, msg, time_taken, counterexample)
            elif result_from_stdout == RESULT_UNKNOWN:
                result = (RESULT_UNKNOWN, "Verification result unknown", time_taken, None)
            # Check for errors in output
            elif 'ERROR' in stdout or 'ERROR' in stderr or 'Exception' in stderr:
                error_msg = stderr[:500] if stderr else stdout[-500:]
                result = (RESULT_ERROR, f"LEMUR error: {error_msg}", time_taken, None)
            else:
                # Default to unknown if we couldn't determine the result
                result = (RESULT_UNKNOWN, "Could not determine verification result", time_taken, None)
            
            # Keep verification results directory for inspection
            logging.info(f"Verification results preserved in: {temp_work_dir}")
            
            return result
            
        except Exception as e:
            end_time = time.perf_counter()
            # Keep results directory even on exception for debugging
            temp_work_dir = os.path.join(working_dir, os.path.basename(yaml_config_path)[:-4])
            if os.path.exists(temp_work_dir):
                logging.info(f"Exception occurred, results preserved in: {temp_work_dir}")
            return RESULT_ERROR, f"Exception during LEMUR execution: {str(e)}", end_time - start_time, None

def parse_processed_files_from_log(log_file_path: str) -> Dict[str, str]:
    """
    Parse log file to extract already processed files and their results.
    
    Args:
        log_file_path: Path to the log file
        
    Returns:
        Dictionary mapping filename to result status (VERIFIED, FALSIFIED, TIMEOUT, ERROR, UNKNOWN)
    """
    processed_files = {}
    
    if not os.path.exists(log_file_path):
        return processed_files
    
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match result lines
        # Examples:
        # ✓ VERIFIED: term_15
        # ✓ VERIFIED (Lexicographic): term_15
        # ✗ FALSIFIED: term_15
        # ⏱ TIMEOUT: term_15
        # ⚠ ERROR: term_15
        # ? UNKNOWN: term_15
        
        # Parse line by line to preserve order and keep last status
        lines = content.split('\n')
        for line in lines:
            # Try to match each pattern
            if '✓ VERIFIED' in line:
                match = re.search(r'✓ VERIFIED(?:\s+\(Lexicographic\))?: ([\w\-\.\_]+)', line)
                if match:
                    processed_files[match.group(1)] = 'VERIFIED'
            elif '✗ FALSIFIED' in line:
                match = re.search(r'✗ FALSIFIED(?:\s+\(Lexicographic\))?: ([\w\-\.\_]+)', line)
                if match:
                    processed_files[match.group(1)] = 'FALSIFIED'
            elif '⏱ TIMEOUT' in line:
                match = re.search(r'⏱ TIMEOUT(?:\s+\(Lexicographic\))?: ([\w\-\.\_]+)', line)
                if match:
                    processed_files[match.group(1)] = 'TIMEOUT'
            elif '⚠ ERROR' in line:
                match = re.search(r'⚠ ERROR(?:\s+\(Lexicographic\))?: ([\w\-\.\_]+)', line)
                if match:
                    processed_files[match.group(1)] = 'ERROR'
            elif '? UNKNOWN' in line:
                match = re.search(r'\? UNKNOWN(?:\s+\(Lexicographic\))?: ([\w\-\.\_]+)', line)
                if match:
                    processed_files[match.group(1)] = 'UNKNOWN'
        
        logging.info(f"Found {len(processed_files)} processed files in log:")
        for filename, status in processed_files.items():
            logging.info(f"  - {filename}: {status}")
        
    except Exception as e:
        logging.warning(f"Error parsing log file: {e}")
    
    return processed_files


def extract_assume_expressions(text: str) -> Tuple[List[Tuple[str, str]], str]:
    """
    Extract assume expressions from LLM output (for conjunctive bounds).
    Returns list of (variable, bound_expr) tuples and original text.
    """
    assume_pattern = r'assume\s*\((.*?)\)\s*;'
    matches = re.findall(assume_pattern, text, re.DOTALL)
    
    bounds = []
    for match in matches:
        # Parse expressions like "i >= n" into (variable, bound)
        parts = re.split(r'(>=|<=|>|<|==|!=)', match.strip())
        if len(parts) >= 3:
            var = parts[0].strip()
            bound_expr = parts[2].strip()
            bounds.append((var, bound_expr))
    
    return bounds, text


def generate_c_decrement_logic(lexical_loop_bound: List[List[str]], 
                                 itVars: List[str], 
                                 indent: int = 4) -> str:
    """
    Generate C code for lexicographic decrement logic.
    This mimics the Boogie IT (Iteration) code generation.
    
    Args:
        lexical_loop_bound: 2D list of bounds, e.g., [['n-x'], ['10']]
        itVars: List of counter variable names, e.g., ['i0', 'i1']
        indent: Base indentation level
        
    Returns:
        C code string for decrement logic
    """
    def generate_it_code_recursive(now: int, current_indent: int) -> str:
        """Recursively generate nested if-else structure for lexicographic decrement."""
        indent_str = ' ' * current_indent
        indent_inc = ' ' * (current_indent + 4)
        
        if now == 0:
            # Base case: just decrement the lowest counter
            return f"{indent_str}{itVars[now]} = {itVars[now]} - 1;\n"
        
        # Build the ranking bound condition
        ranking_bounds = []
        for bound in lexical_loop_bound[now]:
            ranking_bounds.append(f"{itVars[now]} >= {bound}")
        ranking_condition = ' && '.join(ranking_bounds)
        
        # Generate nested structure
        code = f"{indent_str}if ({itVars[now]} > 0) {{\n"
        code += f"{indent_inc}{itVars[now]} = {itVars[now]} - 1;\n"
        code += f"{indent_str}}} else {{\n"
        code += generate_it_code_recursive(now - 1, current_indent + 4)
        code += f"{indent_inc}// Havoc and assume for {itVars[now]}\n"
        code += f"{indent_inc}// In C, we use nondeterministic value\n"
        code += f"{indent_inc}{itVars[now]} = __VERIFIER_nondet_int();\n"
        code += f"{indent_inc}assume({ranking_condition});\n"
        code += f"{indent_str}}}\n"
        
        return code
    
    if not itVars or not lexical_loop_bound:
        return ""
    
    # Start from the highest counter
    return generate_it_code_recursive(len(itVars) - 1, indent)


def find_bpl_files(directory: str) -> List[str]:
    """Find all .bpl files in directory structure."""
    bpl_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.bpl'):
                bpl_files.append(os.path.join(root, file))
    return bpl_files


def read_file_to_string(filename: str) -> str:
    """Read BPL file content as string."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return ""


def read_file_to_string_c(filename: str, c_benchmarks_dir: str = '/root/LIFT/experiment/benchmarks/C_style') -> str:
    """Read C file content as string."""
    c_file = os.path.join(c_benchmarks_dir, filename + '.c')
    try:
        with open(c_file, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading C file {c_file}: {e}")
        return ""


def remove_empty(s: str) -> str:
    """Remove empty lines and extra whitespace."""
    lines = [line for line in s.split('\n') if line.strip()]
    return '\n'.join(lines)


def setup_logging(log_dir: str, log_filename: str) -> logging.Logger:
    """Setup logging configuration."""
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, log_filename)
    
    logger = logging.getLogger('lemur_verification')
    logger.setLevel(logging.INFO)
    
    # File handler
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.INFO)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger


def load_config(config_path='config.yaml'):
    default_config = {
        'llm_lb': {'type': 1},
        'llm_invariant': {'type': 1},
        'directories': {
            'tmp_dir': '/tmpfs/tmp',
            'input_dir': '/root/LIFT/experiment/benchmarks-Instrumented',
            'c_benchmarks_dir': '/root/LIFT/experiment/benchmarks/C_style'
        },
        'logging': {
            'log_dir': 'logs/lemur_integration',
            'log_filename': 'loop_bound_lemur_verification.log'
        },
        'output': {
            'result_filename': 'results/lemur_integration/loop_bound_lemur_results.txt'
        },
        'verification': {
            'max_conj_iterations': 5,
            'max_lex_iterations': 15,
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
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='LIFT Loop Bound Verification with LEMUR')
    parser.add_argument('-c', '--config', type=str, default='config.yaml',
                        help='Path to configuration YAML file')
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Extract configuration values
    tmpDir = config['directories']['tmp_dir'] + '/lemur_verification'
    c_benchmarks_dir = config['directories'].get('c_benchmarks_dir', '/root/LIFT/experiment/benchmarks/C_style')
    os.makedirs(tmpDir, exist_ok=True)
    
    llm_type = config['llm_lb']['type']
    llm_invariant_type = config.get('llm_invariant', {}).get('type', 1)
    
    out_filename = config['output']['result_filename']
    log_dir = config['logging']['log_dir']
    log_filename = config['logging']['log_filename']
    
    os.makedirs(os.path.dirname(out_filename), exist_ok=True)
    logger = setup_logging(log_dir, log_filename)
    
    # Parse log file for checkpoint resume
    log_file_path = os.path.join(log_dir, log_filename)
    processed_files = parse_processed_files_from_log(log_file_path)
    
    if processed_files:
        logger.info(f"\n{'='*80}")
        logger.info("CHECKPOINT RESUME MODE")
        logger.info(f"{'='*80}")
        logger.info(f"Found {len(processed_files)} already processed files")
        logger.info("These files will be skipped in this run")
    
    # Find C files for loop bound inference and verification
    c_files = []
    for root, dirs, files in os.walk(c_benchmarks_dir):
        for file in files:
            if file.endswith('.c'):
                c_files.append(os.path.join(root, file))
    print(f"Found {len(c_files)} C benchmark files")
    logger.info(f"Found {len(c_files)} C benchmark files")
    
    # Initialize LEMUR verifier
    lemur_verifier = LEMURVerifier()
    
    # Statistics
    success_count = 0
    failure_count = 0
    timeout_count = 0
    error_count = 0
    unknown_count = 0
    skipped_count = 0
    
    # Count already processed files from log
    for status in processed_files.values():
        if status == 'VERIFIED':
            success_count += 1
        elif status == 'FALSIFIED':
            failure_count += 1
        elif status == 'TIMEOUT':
            timeout_count += 1
        elif status == 'ERROR':
            error_count += 1
        elif status == 'UNKNOWN':
            unknown_count += 1
    
    logger.info(f"Starting statistics from checkpoint:")
    logger.info(f"  Verified: {success_count}")
    logger.info(f"  Falsified: {failure_count}")
    logger.info(f"  Timeout: {timeout_count}")
    logger.info(f"  Error: {error_count}")
    logger.info(f"  Unknown: {unknown_count}")
    
    # Process each C benchmark
    for c_file in c_files:  # Limit to first 5 for testing
        last_slash_index = c_file.rfind('/')
        filename = c_file[last_slash_index + 1: -2]
        full_filename = filename + ".c"
        
        # Check if file was already processed (checkpoint resume)
        if filename in processed_files:
            logger.info(f"\n{'='*80}")
            logger.info(f"SKIPPING (already processed): {filename}")
            logger.info(f"  Previous result: {processed_files[filename]}")
            logger.info(f"{'='*80}")
            skipped_count += 1
            continue
        
        logger.info(f"\n{'='*80}")
        logger.info(f"Processing: {filename}")
        
        # Read C code
        try:
            with open(c_file, 'r', encoding='utf-8') as f:
                c_code = f.read()
        except Exception as e:
            logger.error(f"Failed to read C file for {filename}: {e}")
            error_count += 1
            continue
        
        if not c_code:
            logger.error(f"Empty C benchmark for {filename}")
            error_count += 1
            continue
        
        # Loop bound inference iteration
        # Phase 1: Conjunctive bounds (first 5 iterations)
        # Phase 2: Lexicographic bounds (next 10 iterations)
        iter_back = 0
        max_iterations_conj = 5
        max_iterations_lex = 10
        timeout_per_verification = 60  # Timeout for each verification attempt
        prompt_type = 0
        feed_back_message = ""
        ce = None
        repeat_notice = False
        conj_or_lex = False  # False for conjunctive, True for lexicographic
        previous_llm_answer = []
        previous_loop_bound = []
        previous_lexical_loop_bound = []
        verification_ret = RESULT_UNKNOWN
        
        # Phase 1: Conjunctive loop bounds (C code only)
        logger.info("=== Phase 1: Conjunctive Loop Bounds ===")
        while iter_back < max_iterations_conj and verification_ret != RESULT_VERIFIED:
            # Generate loop bound using LLM
            try:
                if previous_llm_answer:
                    if not repeat_notice:
                        feed_back_message = previous_llm_answer[-1][0]
                        prompt_type = previous_llm_answer[-1][1]
                        ce = previous_llm_answer[-1][2]
                    else:
                        all_history_tmp = list(zip(*previous_llm_answer))
                        all_history = [list(item) for item in all_history_tmp]
                        feed_back_message, prompt_type, ce = all_history
                
                (llm_answer, infer_time, token_usage) = openai_gen_answer(
                    0, llm_type, c_code, conj_or_lex, 
                    prompt_type, feed_back_message, ce, repeat_notice, code_type='C'
                )
                # llm_answer = "assume(i >= 3);"
                # infer_time = 0
                # token_usage = {'total_tokens': 0}
                llm_answer = remove_empty(llm_answer)
                loop_bound, llm_answer = extract_assume_expressions(llm_answer)
                
                logger.info(f"[Conjunctive] LLM suggested loop bound (iteration {iter_back}): {llm_answer}")
                logger.info(f"[Conjunctive] Extracted bounds: {loop_bound}")
                
                if not loop_bound:
                    logger.warning("No valid loop bound extracted from LLM answer")
                    prompt_type = 1
                    previous_llm_answer.append([str(llm_answer), prompt_type, None])
                    iter_back += 1
                    continue
                
                # Check for duplicate
                if loop_bound in previous_loop_bound:
                    logger.info(f"Loop bound {llm_answer} has already been tried.")
                    repeat_notice = True
                    iter_back += 1
                    continue
                repeat_notice = False
                previous_loop_bound.append(loop_bound)
                
            except Exception as e:
                logger.error(f"Error during loop bound inference: {e}")
                error_count += 1
                break
            
            # Try CBC verification first for simple numeric bounds
            if len(loop_bound) == 1:
                simple_bound = loop_bound[0][1]
                if simple_bound.isdigit():
                    simple_bound_val = int(simple_bound)
                    if simple_bound_val < 100000:  # CBC should not be too large
                        logger.info(f"Attempting CBC verification with bound: {simple_bound_val}")
                        try:
                            base_dir = "/root/LIFT/experiment/benchmarks-Instrumented/"
                            boogie_file = base_dir + filename + "/" + filename + ".bpl"
                            filtered_bpl = os.path.join("/tmpfs/tmp", f"{filename}.bpl")
                            copy_bpl_without_pattern(boogie_file, filtered_bpl, pattern="i%")
                            # Use the actual c_file path instead of constructing from inputdir
                            cbcchecker = CBChecker("/tmpfs/tmp", filtered_bpl, itvar='i')
                            cbc_ret = cbcchecker.ExecuteCBC(simple_bound_val, timeout=timeout_per_verification, timeoutMonitor='/usr/bin/timeout')
                            
                            if cbc_ret == 1:
                                logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, invariant: CBC Bound-- {simple_bound_val}, k: 0, invariant: None, verification_time: {cbcchecker.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                                success_count += 1
                                verification_ret = RESULT_VERIFIED
                                break
                            elif cbc_ret == 2:
                                logger.info(f"CBC verification failed with the loop bound: {llm_answer}, file: {full_filename} , k: 0, feed_back_iter: {iter_back}, verification_time: {cbcchecker.time}, infer_time: {infer_time}, tokens: {token_usage['total_tokens']}")
                                # Try with constant +3
                                simple_bound_val_plus3 = simple_bound_val + 3
                                cbc_ret = cbcchecker.ExecuteCBC(simple_bound_val_plus3, timeout=timeout_per_verification, timeoutMonitor='/usr/bin/timeout')
                                if cbc_ret == 1:
                                    logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, invariant: CBC Bound-- {simple_bound_val_plus3}, k: 0, invariant: None, verification_time: {cbcchecker.time}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                                    success_count += 1
                                    verification_ret = RESULT_VERIFIED
                                    break
                                elif cbc_ret == 2:
                                    logger.info(f"CBC verification failed after adding const with the loop bound: {llm_answer}, file: {full_filename} , k: 0, feed_back_iter: {iter_back}, verification_time: {cbcchecker.time}, infer_time: {infer_time}, tokens: {token_usage['total_tokens']}")
                                    prompt_type = 2
                                    previous_llm_answer.append([str(llm_answer), prompt_type, None])
                                    iter_back += 1
                                    continue
                                elif cbc_ret == 3:
                                    logger.info(f"CBC verification timed out after adding const with the loop bound: {llm_answer}, file: {full_filename}, k: 0, feed_back_iter: {iter_back}, verification_time: {cbcchecker.time}, infer_time: {infer_time}, tokens: {token_usage['total_tokens']}")
                            elif cbc_ret == 3:
                                logger.info(f"CBC verification timed out with the loop bound: {llm_answer}, file: {full_filename}, k: 0, feed_back_iter: {iter_back}, verification_time: {cbcchecker.time}, infer_time: {infer_time}, tokens: {token_usage['total_tokens']}")
                        except Exception as e:
                            logger.warning(f"CBC verification error: {e}, falling back to LEMUR")
            
            # Create modified C file with assume statements for LEMUR
            try:
                modified_c_file = os.path.join(tmpDir, f"{filename}_bounded.c")
                assumptions = [f"assume({var} >= {bound});" for var, bound in loop_bound]
                
                success = lemur_verifier.create_c_with_loop_bound(
                    c_file, modified_c_file, assumptions
                )
                
                if not success:
                    logger.error("Failed to create modified C file")
                    error_count += 1
                    break
                
                logger.info(f"Created modified C file with assumptions: {assumptions}")
                
            except Exception as e:
                logger.error(f"Error creating modified C file: {e}")
                error_count += 1
                break
            
            # Create YAML config
            try:
                yaml_config = os.path.join(tmpDir, f"{filename}.yml")
                success = lemur_verifier.create_yaml_config(
                    modified_c_file, yaml_config, tmpDir, property_type='reach'
                )
                
                if not success:
                    logger.error("Failed to create YAML config")
                    error_count += 1
                    break
                
            except Exception as e:
                logger.error(f"Error creating YAML config: {e}")
                error_count += 1
                break
            
            # Run LEMUR
            try:
                working_dir = os.path.join(tmpDir, f'lemur_work_{filename}_conj_iter_{iter_back}')
                os.makedirs(working_dir, exist_ok=True)
                
                result_code, message, time_taken, counterexample = lemur_verifier.run_lemur(
                    yaml_config, working_dir, 
                    model=llm_model_for_lemur,
                    per_instance_timeout=60,
                    iteration=iter_back
                )
                
                # Log and count results with consistent format
                if result_code == RESULT_VERIFIED:
                    logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, invariant: {message}, verification_time: {time_taken}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                    success_count += 1
                    verification_ret = RESULT_VERIFIED
                    break
                    
                elif result_code == RESULT_UNKNOWN or result_code == RESULT_TIMEOUT:
                    status_text = "unknown" if result_code == RESULT_UNKNOWN else "timed out"
                    logger.info(f"Verification {status_text} with the loop bound: {llm_answer}, file: {full_filename}, verification_time: {time_taken}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                    prompt_type = 3
                    previous_llm_answer.append([llm_answer, prompt_type, None])
                    
                elif result_code == RESULT_FALSIFIED:
                    logger.info(f"Verification failed with the loop bound: {llm_answer}, file: {full_filename}, verification_time: {time_taken}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                    
                    # Always try with constant +3 added to bounds
                    logger.info(f"Attempting const-add verification with +3 for loop bound: {llm_answer}")
                    new_loop_bound = []
                    for var, bound in loop_bound:
                        new_bound = (var, bound + '+3')
                        new_loop_bound.append(new_bound)
                    
                    try:
                        # Create modified C file with +3 bounds
                        modified_c_file_plus3 = os.path.join(tmpDir, f"{filename}_bounded_plus3.c")
                        assumptions_plus3 = [f"assume({var} >= {bound});" for var, bound in new_loop_bound]
                        
                        success = lemur_verifier.create_c_with_loop_bound(
                            c_file, modified_c_file_plus3, assumptions_plus3
                        )
                        
                        if success:
                            yaml_config_plus3 = os.path.join(tmpDir, f"{filename}_plus3.yml")
                            success = lemur_verifier.create_yaml_config(
                                modified_c_file_plus3, yaml_config_plus3, tmpDir, property_type='reach'
                            )
                            
                            if success:
                                working_dir_plus3 = os.path.join(tmpDir, f'lemur_work_{filename}_conj_iter_{iter_back}_plus3')
                                os.makedirs(working_dir_plus3, exist_ok=True)
                                
                                result_code_plus3, message_plus3, time_taken_plus3, ce_plus3 = lemur_verifier.run_lemur(
                                    yaml_config_plus3, working_dir_plus3, 
                                    model=llm_model_for_lemur,
                                    per_instance_timeout=60,
                                    iteration=f"{iter_back}_plus3"
                                )
                                
                                if result_code_plus3 == RESULT_VERIFIED:
                                    logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, const_part: 3, invariant: {message_plus3}, verification_time: {time_taken_plus3}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                                    success_count += 1
                                    verification_ret = RESULT_VERIFIED
                                    break
                                else:
                                    status_map = {RESULT_FALSIFIED: "failed", RESULT_TIMEOUT: "timed out", RESULT_UNKNOWN: "unknown", RESULT_ERROR: "error"}
                                    status_text = status_map.get(result_code_plus3, "unknown result")
                                    logger.info(f"Const-add verification {status_text} with the loop bound: {llm_answer}, file: {full_filename}, const_part: 3, verification_time: {time_taken_plus3}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                    except Exception as e:
                        logger.warning(f"Const-add verification error: {e}")
                    
                    prompt_type = 2
                    previous_llm_answer.append([llm_answer, prompt_type, counterexample])
                    
                elif result_code == RESULT_ERROR:
                    logger.info(f"LEMUR error with the loop bound: {llm_answer}, file: {full_filename}, verification_time: {time_taken}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                    prompt_type = 1
                    previous_llm_answer.append([llm_answer, prompt_type, None])
                
            except Exception as e:
                logger.error(f"Error during LEMUR execution: {e}")
                error_count += 1
                break
            
            iter_back += 1
        
        # Phase 2: Lexicographic loop bounds
        if verification_ret != RESULT_VERIFIED:
            logger.info("\n=== Phase 2: Lexicographic Loop Bounds ===")
            conj_or_lex = True
            iter_back = 0
            prompt_type = 0
            ce = None
            repeat_notice = False
            previous_llm_answer = []  # Reset for lexicographic phase
            
            while iter_back < max_iterations_lex and verification_ret != RESULT_VERIFIED:
                # Generate lexicographic loop bound using LLM
                try:
                    if previous_llm_answer:
                        if not repeat_notice:
                            feed_back_message = previous_llm_answer[-1][0]
                            prompt_type = previous_llm_answer[-1][1]
                            ce = previous_llm_answer[-1][2]
                        else:
                            all_history_tmp = list(zip(*previous_llm_answer))
                            all_history = [list(item) for item in all_history_tmp]
                            feed_back_message, prompt_type, ce = all_history
                    
                    (llm_answer, infer_time, token_usage) = openai_gen_answer(
                        0, llm_type, c_code, conj_or_lex,  # Use C code for lexicographic
                        prompt_type, feed_back_message, ce, repeat_notice, code_type='C' 
                    )
                    
                    llm_answer = remove_empty(llm_answer)
                    lexical_loop_bound, llm_answer = extract_lexical_bounds(llm_answer)
                    
                    logger.info(f"[Lexicographic] LLM suggested loop bound (iteration {iter_back}): {llm_answer}")
                    logger.info(f"[Lexicographic] Extracted bounds: {lexical_loop_bound}")
                    
                    if not lexical_loop_bound:
                        logger.warning("No valid lexical loop bound extracted")
                        prompt_type = 1
                        previous_llm_answer.append([str(llm_answer), prompt_type, None])
                        iter_back += 1
                        continue
                    
                    # Check for duplicate
                    if lexical_loop_bound in previous_lexical_loop_bound:
                        logger.info(f"Lexical loop bound {llm_answer} has already been tried.")
                        repeat_notice = True
                        iter_back += 1
                        continue
                    repeat_notice = False
                    
                    # Check if counter appears in bound (error)
                    num_counters = len(lexical_loop_bound)
                    search_terms = [f'i{j}' for j in range(num_counters)]
                    search_terms.append('i')
                    combined_pattern_str = r'\b(' + '|'.join(search_terms) + r')\b'
                    compiled_pattern = re.compile(combined_pattern_str)
                    
                    if any(compiled_pattern.search(bound) for counter in lexical_loop_bound for bound in counter):
                        logger.warning("Counter variable found in bound expression")
                        prompt_type = 1
                        previous_llm_answer.append([str(llm_answer), prompt_type, None])
                        iter_back += 1
                        continue
                    
                    previous_lexical_loop_bound.append(lexical_loop_bound)
                    
                    # Generate counter variables
                    itvar = 'i'
                    itVars = lex_counter_distill(lexical_loop_bound, itvar)
                    
                    if not itVars:
                        logger.error("Failed to generate counter variables")
                        prompt_type = 1
                        previous_llm_answer.append([str(llm_answer), prompt_type, None])
                        iter_back += 1
                        continue
                    
                    logger.info(f"[Lexicographic] Counter variables: {itVars}")
                    
                except Exception as e:
                    logger.error(f"Error during lexicographic loop bound inference: {e}")
                    import traceback
                    traceback.print_exc()
                    error_count += 1
                    break
                
                # Create modified C file with lexicographic bound
                try:
                    modified_c_file = os.path.join(tmpDir, f"{filename}_lex_bounded.c")
                    
                    # Build assumptions for counter initializations
                    assumptions = []
                    for i, var in enumerate(itVars):
                        for bound in lexical_loop_bound[i]:
                            assumptions.append(f"assume({var} >= {bound});")
                    
                    success = lemur_verifier.create_c_with_loop_bound(
                        c_file, modified_c_file, assumptions,
                        is_lexicographic=True,
                        lexical_loop_bound=lexical_loop_bound,
                        itVars=itVars
                    )
                    
                    if not success:
                        logger.error("Failed to create modified C file with lexicographic bound")
                        error_count += 1
                        break
                    
                    logger.info(f"Created modified C file with lexicographic bound")
                    logger.info(f"  Counters: {itVars}")
                    logger.info(f"  Bounds: {lexical_loop_bound}")
                    
                except Exception as e:
                    logger.error(f"Error creating modified C file: {e}")
                    import traceback
                    traceback.print_exc()
                    error_count += 1
                    break
                
                # Create YAML config
                try:
                    yaml_config = os.path.join(tmpDir, f"{filename}_lex.yml")
                    success = lemur_verifier.create_yaml_config(
                        modified_c_file, yaml_config, tmpDir, property_type='reach'
                    )
                    
                    if not success:
                        logger.error("Failed to create YAML config")
                        error_count += 1
                        break
                    
                except Exception as e:
                    logger.error(f"Error creating YAML config: {e}")
                    error_count += 1
                    break
                
                # Run LEMUR
                try:
                    working_dir = os.path.join(tmpDir, f'lemur_work_{filename}_lex_iter_{iter_back}')
                    os.makedirs(working_dir, exist_ok=True)
                    
                    result_code, message, time_taken, counterexample = lemur_verifier.run_lemur(
                        yaml_config, working_dir, 
                        model=llm_model_for_lemur,
                        per_instance_timeout=60,
                        iteration=iter_back
                    )
                    
                    # Log and count results with consistent format
                    if result_code == RESULT_VERIFIED:
                        logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, k: lexicographic, invariant: {message}, verification_time: {time_taken}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        success_count += 1
                        verification_ret = RESULT_VERIFIED
                        break
                        
                    elif result_code == RESULT_UNKNOWN or result_code == RESULT_TIMEOUT:
                        status_text = "unknown" if result_code == RESULT_UNKNOWN else "timed out"
                        logger.info(f"Verification {status_text} with the loop bound: {llm_answer}, file: {full_filename}, k: lexicographic, verification_time: {time_taken}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        prompt_type = 3
                        previous_llm_answer.append([llm_answer, prompt_type, None])
                        
                    elif result_code == RESULT_FALSIFIED:
                        logger.info(f"Verification failed with the loop bound: {llm_answer}, file: {full_filename}, k: lexicographic, verification_time: {time_taken}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        
                        # Always try with constant +3 added to all bounds
                        logger.info(f"Attempting const-add lexicographic verification with +3 for loop bound: {llm_answer}")
                        new_lexi_loop_bound = []
                        for counter in lexical_loop_bound:
                            new_lexi_counter = []
                            for bound in counter:
                                new_lexi_counter.append(bound + '+3')
                            new_lexi_loop_bound.append(new_lexi_counter)
                        
                        try:
                            # Create modified C file with +3 bounds
                            modified_c_file_plus3 = os.path.join(tmpDir, f"{filename}_lex_bounded_plus3.c")
                            assumptions_plus3 = []
                            for i, var in enumerate(itVars):
                                for bound in new_lexi_loop_bound[i]:
                                    assumptions_plus3.append(f"assume({var} >= {bound});")
                            
                            success = lemur_verifier.create_c_with_loop_bound(
                                c_file, modified_c_file_plus3, assumptions_plus3,
                                is_lexicographic=True,
                                lexical_loop_bound=new_lexi_loop_bound,
                                itVars=itVars
                            )
                            
                            if success:
                                yaml_config_plus3 = os.path.join(tmpDir, f"{filename}_lex_plus3.yml")
                                success = lemur_verifier.create_yaml_config(
                                    modified_c_file_plus3, yaml_config_plus3, tmpDir, property_type='reach'
                                )
                                
                                if success:
                                    working_dir_plus3 = os.path.join(tmpDir, f'lemur_work_{filename}_lex_iter_{iter_back}_plus3')
                                    os.makedirs(working_dir_plus3, exist_ok=True)
                                    
                                    result_code_plus3, message_plus3, time_taken_plus3, ce_plus3 = lemur_verifier.run_lemur(
                                        yaml_config_plus3, working_dir_plus3, 
                                        model=llm_model_for_lemur,
                                        per_instance_timeout=60,
                                        iteration=f"{iter_back}_plus3"
                                    )
                                    
                                    if result_code_plus3 == RESULT_VERIFIED:
                                        logger.info(f"Verification succeeded with the loop bound: {llm_answer}, file: {full_filename}, const_part: 3, invariant: {message_plus3}, verification_time: {time_taken_plus3}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                                        success_count += 1
                                        verification_ret = RESULT_VERIFIED
                                        break
                                    else:
                                        status_map = {RESULT_FALSIFIED: "failed", RESULT_TIMEOUT: "timed out", RESULT_UNKNOWN: "unknown", RESULT_ERROR: "error"}
                                        status_text = status_map.get(result_code_plus3, "unknown result")
                                        logger.info(f"Const-add lexical verification {status_text} with the loop bound: {llm_answer}, file: {full_filename}, const_part: 3, verification_time: {time_taken_plus3}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        except Exception as e:
                            logger.warning(f"Const-add lexicographic verification error: {e}")
                        
                        prompt_type = 2
                        previous_llm_answer.append([llm_answer, prompt_type, counterexample])
                        
                    elif result_code == RESULT_ERROR:
                        logger.info(f"LEMUR error with the loop bound: {llm_answer}, file: {full_filename}, k: lexicographic, verification_time: {time_taken}, infer_time: {infer_time}, feed_back_iter: {iter_back}, tokens: {token_usage['total_tokens']}")
                        prompt_type = 1
                        previous_llm_answer.append([llm_answer, prompt_type, None])
                    
                except Exception as e:
                    logger.error(f"Error during LEMUR execution: {e}")
                    import traceback
                    traceback.print_exc()
                    error_count += 1
                    break
                
                iter_back += 1
        
        # Count final result if not verified
        if verification_ret != RESULT_VERIFIED:
            if result_code == RESULT_TIMEOUT:
                timeout_count += 1
            elif result_code == RESULT_FALSIFIED:
                failure_count += 1
            elif result_code == RESULT_ERROR:
                error_count += 1
            else:
                unknown_count += 1
    
    # Write summary
    logger.info(f"\n{'='*80}")
    logger.info("VERIFICATION SUMMARY")
    logger.info(f"{'='*80}")
    logger.info(f"Total files found: {len(c_files)}")
    logger.info(f"⏭ Skipped (from checkpoint): {skipped_count}")
    logger.info(f"🔄 Processed in this run: {len(c_files) - skipped_count}")
    logger.info(f"")
    logger.info(f"Overall Results:")
    logger.info(f"✓ Verified: {success_count}")
    logger.info(f"✗ Falsified: {failure_count}")
    logger.info(f"⏱ Timeout: {timeout_count}")
    logger.info(f"⚠ Error: {error_count}")
    logger.info(f"? Unknown: {unknown_count}")
    
    with open(out_filename, 'w', encoding='utf-8') as f:
        f.write(f"LEMUR Integration Results\n")
        f.write(f"={'='*60}\n")
        f.write(f"Total files: {len(c_files)}\n")
        f.write(f"Skipped (checkpoint): {skipped_count}\n")
        f.write(f"Processed this run: {len(c_files) - skipped_count}\n")
        f.write(f"\n")
        f.write(f"Overall Results:\n")
        f.write(f"Verified: {success_count}\n")
        f.write(f"Falsified: {failure_count}\n")
        f.write(f"Timeout: {timeout_count}\n")
        f.write(f"Error: {error_count}\n")
        f.write(f"Unknown: {unknown_count}\n")
