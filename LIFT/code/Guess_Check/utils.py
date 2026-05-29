import os
import re
from typing import Tuple, Optional, List
import logging

RESULT_TIMEOUT = 0
RESULT_VERIFIED = 1
RESULT_ERROR = 2
RESULT_INV_FAILED_HOLD = 3
RESULT_INV_FAILED_MAINTAIN = 4
RESULT_ASSERT_FAILED_HOLD = 5

def setup_logging(log_dir='logs', log_filename="verification.log"):
        """Setup logging for the verifier"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        # Ensure log directory exists
        os.makedirs(log_dir, exist_ok=True)
        # Create file handler
        log_filename = os.path.join(log_dir, log_filename)
    
        # Configure logger
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                # Console output
                #logging.StreamHandler(),
                # File output
                logging.FileHandler(log_filename, encoding='utf-8')
            ]
        )
        # Suppress httpx library logs (commonly used for Google API clients and requests)
        # Set level to WARNING to only log warnings and above
        logging.getLogger("httpx").setLevel(logging.WARNING)
        return logging.getLogger(__name__)

def find_bpl_files(directory):
    """
    Recursively find all .bpl files in the given directory and its subdirectories.
    
    Args:
        directory (str): The root directory to start searching from.
    
    Returns:
        list: A list of absolute paths to .bpl files.
    """
    # List to store absolute paths of .bpl files
    bpl_files = []
    
    # Walk through the directory tree
    for root, dirs, files in os.walk(directory):
        # Find .bpl files in the current directory
        for file in files:
            if file.endswith('.bpl'):
                # Get the full absolute path of the .bpl file
                bpl_file_path = os.path.abspath(os.path.join(root, file))
                bpl_files.append(bpl_file_path)
    
    return bpl_files

def extract_assume_expressions(llm_answer, max_len: int = 200):
    """
    Extract all complete assume(...); statements from LLM answer and parse into (i, expression) tuple list.
    
    Args:
        llm_answer: LLM answer string, may contain multiple assume statements
        max_len: Maximum length threshold for assume statement content, statements exceeding this are skipped (default 200)
    
    Returns:
        tuple: (result, assume_statements)
            - result: List of tuples, each in format ('i', expression)
            - assume_statements: Extracted complete assume statement string (multiple statements concatenated)
    """
    # Use balanced parenthesis matching to extract all complete assume(...); statements
    assume_contents = []
    assume_statements = []  # Store complete assume statements
    pattern = r'assume\('
    
    for match in re.finditer(pattern, llm_answer):
        start_pos = match.end()  # Position after 'assume('
        paren_count = 1
        i = start_pos
        
        # Match balanced parentheses
        while i < len(llm_answer) and paren_count > 0:
            if llm_answer[i] == '(':
                paren_count += 1
            elif llm_answer[i] == ')':
                paren_count -= 1
            i += 1
        
        # Check if it ends with semicolon
        if paren_count == 0 and i < len(llm_answer) and llm_answer[i] == ';':
            # Found complete assume(...);
            assume_content = llm_answer[start_pos:i-1].strip()  # Exclude final ')'
            full_statement = f"assume({assume_content});"  # Complete assume statement
            assume_contents.append(assume_content)
            assume_statements.append(full_statement)
    
    # Process all extracted assume statements
    predicates = []
    result = []
    valid_statements = []  # Only keep non-filtered statements
    
    for idx, assume_content in enumerate(assume_contents):
        # Skip overly long segments containing redundant information
        if len(assume_content) > max_len:
            continue
        
        valid_statements.append(assume_statements[idx])
        
        # Remove whitespace from the expression
        cleaned_expr = re.sub(r'\s+', '', assume_content)
        
        # Split by top-level '&&' into multiple predicates
        predicates.extend(split_at_top_level_and(cleaned_expr))
    
    # Parse each predicate, extract i >= expression format
    for predicate in predicates:
        if predicate[0] == '(':
            index_l = 4
            index_r = len(predicate) - 1
        else:
            index_l = 3
            index_r = len(predicate)
        result.append(('i', predicate[index_l: index_r]))
    
    # Concatenate all valid assume statements into a single string
    return result, ' '.join(valid_statements)


def extract_lexical_bounds(content, max_len: int = 200):
    """
    Extract expressions on the right side of inequalities from strings containing 'assume' statements,
    and organize them into a 2D list.

    Args:
        content: String containing 'assume' statements, e.g., 'assume(i0 >= x + 2 && i1 >= 10);'
        max_len: Maximum length threshold for assume statement content, statements exceeding this are skipped (default 200)

    Returns:
        tuple: (result, assume_statements)
            - result: A 2D list where each inner list corresponds to a counter,
                     containing the expressions on the right side of that counter's inequalities.
                     E.g., for 'assume(i0 >= x + 2 && i1 >= 10);', returns [[x+2], [10]]
            - assume_statements: Extracted complete assume statement string (multiple statements concatenated)
    """
    # Use balanced parenthesis matching to extract all complete assume(...); statements
    # This correctly handles nested parentheses and multiple assume statements
    assume_contents = []
    assume_statements = []  # Store complete assume statements
    pattern = r'assume\('
    
    for match in re.finditer(pattern, content):
        start_pos = match.end()  # Position after 'assume('
        paren_count = 1
        i = start_pos
        
        # Match balanced parentheses
        while i < len(content) and paren_count > 0:
            if content[i] == '(':
                paren_count += 1
            elif content[i] == ')':
                paren_count -= 1
            i += 1
        
        # Check if it ends with semicolon
        if paren_count == 0 and i < len(content) and content[i] == ';':
            # Found complete assume(...);
            assume_content = content[start_pos:i-1].strip()  # Exclude final ')'
            full_statement = f"assume({assume_content});"  # Complete assume statement
            assume_contents.append(assume_content)
            assume_statements.append(full_statement)

    # Create a dictionary to group inequalities by counter
    counter_bounds = {}
    valid_statements = []  # Only keep non-filtered statements

    for idx, assume_content in enumerate(assume_contents):
        # Skip overly long segments containing redundant information
        if len(assume_content) > max_len:
            continue

        valid_statements.append(assume_statements[idx])

        # Split assume statement content by top-level '&&' into multiple inequalities
        inequalities = split_at_top_level_and(assume_content)

        for ineq in inequalities:
            ineq = ineq.strip()
            # Use regex to extract counter name and expression on right side of inequality
            ineq_match = re.search(r"([a-zA-Z0-9]+)\s*>=\s*(.+)", ineq)
            if not ineq_match:
                continue  # Skip if inequality format is incorrect

            counter = ineq_match.group(1).strip()  # Counter name (e.g., i0, i1)
            bound = ineq_match.group(2).strip()  # Expression on right side of inequality (e.g., x + 2, 10)
            bound = bound.replace('/', 'div')
            # Add expression to the corresponding counter's list
            if counter not in counter_bounds:
                counter_bounds[counter] = []
            counter_bounds[counter].append(bound)

    if not counter_bounds:
        return [], ""  # Return empty list and empty string if no valid assume statements found

    # Convert dictionary to 2D list
    result = []
    for counter in sorted(counter_bounds.keys()):  # Ensure consistent counter order
        result.append(counter_bounds[counter])

    # Concatenate all valid assume statements into a single string
    return result, ' '.join(valid_statements)

def read_file_to_string(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def read_file_to_string_c(filename):
    base = '/root/LIFT/experiment/benchmarks/C_style/'
    filename = base + filename + '.c'
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"
    
def read_concret_file2string(filename):
    base = '/tmpfs/tmp/'
    filename = base + filename
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return "Error: File not found"
    except Exception as e:
        return f"Error reading file: {str(e)}"
    
def split_at_top_level_and(expression: str):
    """
    Splits an expression string by '&&' only when '&&' is not enclosed
    within parentheses. Handles nested parentheses.

    Args:
        expression: The expression string to split.

    Returns:
        A list of predicate strings, stripped of leading/trailing whitespace.
        Returns a list containing the original stripped expression if no
        top-level '&&' is found.
    """
    predicates = []
    paren_level = 0
    current_start = 0
    for i, char in enumerate(expression):
        if char == '(':
            paren_level += 1
        elif char == ')':
            # Ensure level doesn't go below 0, handles mismatched parens somewhat
            if paren_level > 0:
                paren_level -= 1
        elif char == '&' and i + 1 < len(expression) and expression[i+1] == '&':
            # Check if we are at the top level (paren_level == 0)
            if paren_level == 0:
                # Extract the predicate found before '&&'
                predicates.append(expression[current_start:i].strip())
                # Update the start for the next predicate, skipping '&&'
                current_start = i + 2
    # Add the remaining part of the expression after the last '&&'
    # or the whole expression if no top-level '&&' was found
    last_part = expression[current_start:].strip()
    if last_part:
      predicates.append(last_part)

    # If the input expression had no top-level '&&', the list will contain
    # just the original (stripped) expression.
    # Return only non-empty results
    return [p for p in predicates if p]

def remove_empty(str):
    str = str.replace('`', '')
    str = str.replace('boogie', '')
    str = str.replace('\n', '')
    return str


def parse_llm_loop_bound_output(llm_output: str) -> Optional[Tuple[int, str]]:
  """
  Strictly parses the LLM output string to extract the loop bound type and content.

  Args:
    llm_output: The string output from the LLM, expected in the format
                "loop bound type: T, content: 'assume(...)'".

  Returns:
    A tuple containing:
      - An integer representing the loop bound type (0 or 1).
      - A string containing the assume statement (e.g., "assume(...)").
    Returns None if the input string does not match the expected format.
  """
  pattern = r"loop bound type:\s*(\d+)\s*,\s*content:\s*'(assume(.*))'"

  match = re.search(pattern, llm_output.strip()) # Use strip() to remove leading/trailing whitespace

  if match:
    try:
      type_str = match.group(1)
      content_str = match.group(2)
      type_int = int(type_str)
      if type_int not in [0, 1]:
          print(f"Warning: Extracted type '{type_int}' is not 0 or 1.")
      return (type_int, content_str)
    except (ValueError, IndexError):
      print(f"Error processing matched string: {llm_output}")
      return None
  print(f"Error: Input string does not match expected format: '{llm_output}'")
  return None


def parse_llm_loop_bound_output_lenient(llm_output: str) -> Optional[Tuple[int, str]]:
  """
  Lenient parser for LLM loop bound output with heuristic recovery.

  - First tries the strict parser.
  - If it fails, attempts to recover an assume expression and infer type from counters.
  """
  strict_result = parse_llm_loop_bound_output(llm_output)
  if strict_result is not None:
      return strict_result

  assume_pattern = r"assume\s*\(.*\);"
  assume_match = re.search(assume_pattern, llm_output)
  if assume_match:
      content_str = assume_match.group(0)
      if 'i0' in content_str or 'i1' in content_str:
          type_int = 1
      else:
          type_int = 0
      print(f"Heuristic parse success: type {type_int}, content '{content_str}'")
      return (type_int, content_str)

  print(f"Error: Input string does not match expected format: '{llm_output}'")
  return None

def lex_counter_distill(lexRank, itVar):
    itVars = []
    rankValue = len(lexRank)
    if rankValue == 1:
        itVars.append(itVar)
    else:
        for i in range(rankValue):
            itVars.append(itVar+'{}'.format(i))
    return itVars

def is_parentheses_balanced(s):
    stack = []
    
    matching_parentheses = {')': '(', ']': '[', '}': '{'}
    
    for char in s:

        if char in '({[':
            stack.append(char)

        elif char in ')}]':

            if not stack or stack[-1] != matching_parentheses[char]:
                return False

            stack.pop()

def is_properly_enclosed(s: str) -> bool:
    """
    Check if a string is enclosed by a pair of matching parentheses that wrap the entire content.
    """
    s = s.strip()
    
    # Condition 1: Must start with '(' and end with ')', and length must be at least 2
    if not (len(s) >= 2 and s.startswith('(') and s.endswith(')')):
        return False

    # Check if internal parentheses are balanced
    # We only check s[1:-1] (content after removing outermost parentheses)
    balance = 0
    
    # Iterate through each character of the internal string
    for char in s[1:-1]:
        if char == '(':
            balance += 1
        elif char == ')':
            balance -= 1
        
        # If balance < 0, there's an unmatched right parenthesis, e.g., ")("
        # If balance == 0, parentheses closed mid-way, e.g., "(a)(b)"
        # Both cases violate the "single wrapper" principle
        if balance < 0:
            return False
        
    # After iterating all internal chars, if balance == 0, internal is fully balanced
    # Combined with the already verified outermost parentheses, the string is properly wrapped
    return balance == 0

def undefined_function(subassertion):
    cannot_exsit=['min', '?', 'max', 'unknown', 'factorial', 'pow', 'for', '=>', 'old', 'INT', '->>', '->']
    for cannot_exist_function in cannot_exsit:
        if str(cannot_exist_function) in subassertion:
            return False
    return True

def extract_invariant_statements(text):
    
    # Define a regular expression pattern to match assert statements
    pattern = r"invariant \[(.*?)\];"
    
    # Find all occurrences of the pattern in the text
    match = re.search(pattern, text, flags=re.DOTALL)
    result = None
    if match:
        result = 'invariant (' + match.group(1) + ');'
    # Format the matches as assert statements and return them
    return result

def remove_assert_lines(source_path: str, destination_path: str):
  """
  Read a file, remove lines starting with 'assert' (ignoring leading whitespace),
  then write the result to a new file.

  Args:
    source_path (str): Path to the source file.
    destination_path (str): Path to the destination file to save results.
  """
  try:
    with open(source_path, 'r', encoding='utf-8') as source_file, \
         open(destination_path, 'w', encoding='utf-8') as dest_file:
      
      for line in source_file:
        # Use lstrip() to remove leading whitespace (spaces, tabs)
        # Then check if the line starts with 'assert'.
        if not line.lstrip().startswith('assert'):
          # If not starting with 'assert', write the original line to new file.
          dest_file.write(line)
          
    #print(f"File with assert statements removed saved to: {destination_path}")

  except FileNotFoundError:
    print(f"Error: Source file '{source_path}' not found")
  except Exception as e:
    print(f"Error occurred: {e}")

def remove_invariant_lines(filepath: str):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' does not exist.")
    kept_lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f_read:
            for line in f_read:
                # Remove leading whitespace and trailing newline for precise 'startswith' check.
                # Note: We only use stripped_line to determine whether to keep,
                # if keeping, use the original line (with its original indentation and newline).
                stripped_line = line.lstrip().strip('\n')
                
                if not stripped_line.startswith('invariant'):
                    kept_lines.append(line) # Keep original line (with its original indentation and newline)
        
        # Write kept lines back to original file, overwriting original content
        with open(filepath, 'w', encoding='utf-8') as f_write:
            f_write.writelines(kept_lines)
            
    except IOError as e:
        raise IOError(f"I/O error occurred while processing file '{filepath}': {e}")

    #print(f"Lines starting with 'invariant' in file '{filepath}' have been successfully removed.")

def insert_invariant(invariant, k_file_name):
        try:
            # --- Step 1: Read all lines from file ---
            with open(k_file_name, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # --- Step 2: Find the line number of while statement ---
            while_line_index = -1
            for i, line in enumerate(lines):
                # Use regex \bwhile\b to ensure matching the standalone word "while"
                if re.search(r'\bwhile\b', line):
                    while_line_index = i
                    break # Stop after finding the first one, assuming there's only one while

            # --- Step 3: If while is found, insert invariant ---
            if while_line_index != -1:
                # Get indentation of while statement to align invariant with it
                original_line = lines[while_line_index]
                indentation = original_line[:len(original_line) - len(original_line.lstrip())]
                
                # Prepare the line to insert, adding newline
                line_to_insert = f"{indentation}{invariant}\n"
                
                # Insert after the while statement
                lines.insert(while_line_index + 1, line_to_insert)
                
                # --- Step 4: Write modified content back to file ---
                with open(k_file_name, 'w', encoding='utf-8') as f:
                    f.writelines(lines)
                
                #print(f"Successfully inserted {invariant} into file '{k_file_name}'.")
            else:
                print(f"Warning: 'while' statement not found in file '{k_file_name}', file not modified.")

        except FileNotFoundError:
            print(f"Error: File '{k_file_name}' not found.")
        except Exception as e:
            print(f"Error processing file: {e}")

import re

def insert_assert_invariant(invariant, bmc_file, lexical):
    """
    Insert invariant assertions into BMC file.

    This function converts the given invariant into an assert statement,
    and inserts it at two specific positions in the file:
    1. After the first "assume" statement containing variable "i".
    2. Before the second-to-last line of the file.

    Args:
        invariant (str): The invariant string to insert, must start with "invariant".
        bmc_file (str): Path to the target BMC file.
    """
    # 1. Process invariant string, create assert statement
    if invariant.strip().startswith("invariant"):
        expression = invariant.strip()[len("invariant"):].strip()
    else:
        raise ValueError("Invariant must start with 'invariant'")
    
    # Remove possible trailing semicolon
    if expression.endswith(';'):
        expression = expression[:-1].strip()
        
    assert_statement = f"  assert ({expression});\n"

    # 2. Read file content
    try:
        with open(bmc_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{bmc_file}' not found.")
        return

    # Create a new list of lines for modification
    modified_lines = list(lines)

    # 3. Find first assume statement with variable "i", insert assert statement after it
    insertion_point_1 = -1
    counter = 'i'
    if lexical:
        counter = 'i0'
    for i, line in enumerate(modified_lines):
        stripped_line = line.strip()
        # Use regex \bi\b to ensure matching standalone variable "i"
        if stripped_line.startswith("assume") and re.search(r'\b{}\b'.format(counter), stripped_line):
            insertion_point_1 = i + 1  # Target line is the next line
            break  # Stop searching after found

    if insertion_point_1 != -1:
        modified_lines.insert(insertion_point_1, assert_statement)
    else:
        print("Warning: No assume statement containing variable 'i' found in file. Assertion will not be inserted after assume block.")

    # 4. Insert assert statement before the second-to-last line
    num_lines = len(modified_lines)
    if num_lines >= 2:
        # Calculate index of second-to-last line, insert before it
        insertion_point_2 = num_lines - 1
        modified_lines.insert(insertion_point_2, assert_statement)
    # If file has less than 2 lines after first assert insertion, skip this operation
    elif insertion_point_1 == -1 and num_lines < 2:
         print("Warning: File has too few lines, cannot insert assertion at second-to-last line.")


    # 5. Write modified content back to file
    try:
        with open(bmc_file, 'w') as f:
            f.writelines(modified_lines)
        print(f"Successfully inserted assertion into file '{bmc_file}'.")
    except IOError as e:
        print(f"Error: Failed to write to file '{bmc_file}': {e}")


def join_with_proper_parentheses(AnsSet: list) -> str:
    """
    Join elements of a string list with '&&'.
    Before joining, check if each element is already wrapped by a pair of matching parentheses,
    if not, add parentheses to it.
    """
    if not AnsSet:
        return ""
    
    formatted_list = []
    for s in AnsSet:
        '''
        # Call helper function to check
        if is_properly_enclosed(s):
        # If already meets requirements, use directly (strip whitespace)
            formatted_list.append(s.strip())
        else:
        # Otherwise, add parentheses
        '''
        if s:
            formatted_list.append(f"({s.strip()})")
        
    return '&&'.join(formatted_list)

def parse_boogie_errors(lines: str, expected_error_count: int) -> list:
    """
    Parse Boogie verifier error message strings.

    Args:
        lines: String containing Boogie error messages.
        expected_error_count: Expected number of errors to identify.

    Returns:
        A list containing identified error message constants.

    Raises:
        ValueError: If mismatched error messages found or error count differs from expected.
    """
    res = []
    for line in lines:
        if "Error BP5001" in line:
            if "This assertion might not hold." in line:
                res.append(RESULT_ASSERT_FAILED_HOLD)
            else:
                raise ValueError(f"Error BP5001 found without 'This assertion might not hold.' in line: {line}")
        elif "Error BP5004" in line:
            if "This loop invariant might not hold on entry." in line:
                res.append(RESULT_INV_FAILED_HOLD)
            else:
                raise ValueError(f"Error BP5004 found without 'This loop invariant might not hold on entry.' in line: {line}")
        elif "Error BP5005" in line:
            if "This loop invariant might not be maintained by the loop." in line:
                res.append(RESULT_INV_FAILED_MAINTAIN)
            else:
                raise ValueError(f"Error BP5005 found without 'This loop invariant might not be maintained by the loop.' in line: {line}")

    if len(res) != expected_error_count:
        raise ValueError(f"Expected {expected_error_count} errors, but found {len(res)}.")

    return res


def extract_CEmodel(boogie_output: str) -> str:
    """
    Parses the full output from the Boogie verifier and extracts the model section.
    
    The model section is defined as the text between the lines '*** MODEL'
    and '*** END_MODEL'.

    Args:
        boogie_output: A string containing the complete output from Boogie.

    Returns:
        A string containing the extracted model, or an empty string if no model
        section is found.
    """
    model_lines = []
    in_model_section = False
    
    # Split the output into individual lines
    lines = boogie_output
    
    for line in lines:
        # Strip leading/trailing whitespace to make matching exact
        stripped_line = line.strip()
        
        if stripped_line == '*** MODEL':
            # We've found the start of the model, start recording from the *next* line
            in_model_section = True
            continue # Don't include the '*** MODEL' line itself
            
        if stripped_line == '*** END_MODEL':
            # We've found the end, stop recording
            in_model_section = False
            break # No need to process further lines
            
        if in_model_section:
            # If we are inside the model section, append the current line
            model_lines.append(line)
            
    # Join the collected lines back into a single string with newlines
    return "\n".join(model_lines)

def extract_all_CEmodels(boogie_output: str) -> List[str]:
    """
    Parse complete output from Boogie verifier and extract all model sections.
    
    A model section is defined as text between '*** MODEL' and '*** END_MODEL' lines.
    This function can handle cases where the input contains multiple model sections.

    Args:
        boogie_output: A string containing complete Boogie output.

    Returns:
        A list of strings, where each string is an extracted model content.
        If no model section is found, returns an empty list.
    """
    all_models = []
    current_model_lines = []
    in_model_section = False
    
    for line in boogie_output:
        # Strip whitespace for exact matching
        stripped_line = line.strip()
        
        if stripped_line == '*** MODEL':
            # Found start of model, begin recording
            in_model_section = True
            # Clear temp list, prepare for recording new model
            current_model_lines = []
            # Skip the '*** MODEL' line itself
            continue
            
        if stripped_line == '*** END_MODEL':
            # Found end of model
            if in_model_section:
                in_model_section = False
                # Join all collected lines into a string and add to main list
                all_models.append("\n".join(current_model_lines))
                # Don't break here, continue to find next model
            
        if in_model_section:
            # If inside model section, add current line
            current_model_lines.append(line)
            
    return all_models

if __name__ == "__main__":
    # Example usage with your provided text
    # You can comment this out when using the script for real
    example_boogie_output = """
    Boogie program verifier version 2.2.30705.1126, Copyright (c) 2003-2013, Microsoft.
    *** MODEL
    %lbl%@167 -> false
    %lbl%@227 -> false
    %lbl%@264 -> false
    %lbl%+120 -> true
    %lbl%+81 -> true
    %lbl%+83 -> true
    %lbl%+85 -> true
    %lbl%+87 -> false
    c@0 -> 10
    c@1 -> 10
    c@2 -> 11
    i -> 10
    i@0 -> 10
    i@1 -> 9
    x@0 -> (- 1)
    x@1 -> 0
    x@2 -> (- 10)
    tickleBool -> {
    else -> true
    }
    *** END_MODEL
    *** MODEL
    %lbl%@167 -> false
    %lbl%@227 -> false
    %lbl%@264 -> true
    %lbl%+120 -> true
    %lbl%+81 -> true
    %lbl%+83 -> false
    %lbl%+85 -> false
    %lbl%+87 -> false
    c@0 -> 10
    c@1 -> 0
    c@2 -> 0
    i -> 9
    i@0 -> 0
    i@1 -> 0
    x@0 -> (- 2)
    x@1 -> 0
    x@2 -> 0
    tickleBool -> {
    else -> true
    }
    *** END_MODEL
    /root/LIFT/test.bpl(11,3): Error BP5004: This loop invariant might not hold on entry.
    Execution trace:
        /root/LIFT/test.bpl(5,3): anon0
    /root/LIFT/test.bpl(11,3): Error BP5005: This loop invariant might not be maintained by the loop.
    Execution trace:
        /root/LIFT/test.bpl(5,3): anon0
        /root/LIFT/test.bpl(10,3): anon2_LoopHead
        /root/LIFT/test.bpl(13,5): anon2_LoopBody

    Boogie program verifier finished with 0 verified, 2 errors
    """
    #print("--- Running on built-in example ---")
    #example_boogie_output = example_boogie_output.split('\n')
    #extracted_example = extract_all_CEmodels(example_boogie_output)
    #print(extracted_example)
    #print("\n--- Script is ready to use via command line ---")
    invariant = "invariant i >= 2 || (i == 1 && x <= -50);"
    #inv = extract_invariant_statements(invariant)
    #print(inv)
    # To run for real, you would typically run the main() function
    # main()
    bmc_file = '/tmpfs/tmp/CBC_AliasDarteFeautrierGonnord-SAS2010-speedFails4_true-termination.bpl'
    #insert_assert_invariant(invariant, bmc_file)
    llm_answer = "To prove termination using lexicographical loop bounds, we need to find a tuple of expressions (i0, i1, i2) that decreases with respect to lexicographical order in each iteration of the while loop, and where each component remains non-negative. The assume statement will provide initial bounds for these counters.Let's analyze the loop condition x > 0 && y > 0 && z > 0 and the updates to variables x, y, z within the loop:1.  **Loop Condition:** x > 0 && y > 0 && z > 0. This implies that x, y, z are always at least 1 when the loop continues.2.  **Case 1: x = x - 1;**    *   x decreases by 1.    *   y remains unchanged.    *   z remains unchanged.3.  **Case 2: y = y - 1; z = __VERIFIER_nondet_int();**    *   y decreases by 1.    *   z is assigned a non-deterministic integer. For the loop to continue, z must remain greater than 0, so the new z is at least 1.    *   x remains unchanged.4.  **Case 3: z = z - 1; x = __VERIFIER_nondet_int();**    *   z decreases by 1.    *   x is assigned a non-deterministic integer. For the loop to continue, x must remain greater than 0, so the new x is at least 1.    *   y remains unchanged.We need to choose i0, i1, i2 and their corresponding bound expressions m0(X), m1(X), m2(X).*   **Identifying i0 (Highest Priority Counter):**    y is the best candidate for i0 because it only ever decreases (Case 2) or remains unchanged (Cases 1 & 3). It is never assigned a non-deterministic value. So, i0 maps to y. Thus, m0(X) = y.*   **Identifying i1 (Middle Priority Counter):**    z is a candidate for i1.    *   If y decreases (Case 2, i0 decreases), then z is assigned __VERIFIER_nondet_int(). When i0 decreases, i1 is reset, and assume(i >= m1(X)) is enforced. Since z becomes non-deterministic but must satisfy z > 0, the minimum bound m1(X) must be 1.    *   If y does not decrease, and z decreases (Case 3, i1 decreases), then x is assigned __VERIFIER_nondet_int(). i1 is decremented in this case.    So, i1 maps to z, but its reset bound m1(X) must be 1.*   **Identifying i2 (Lowest Priority Counter):**    x is a candidate for i2.    *   If y decreases (Case 2, i0 decreases), i2 is reset. x is unchanged. However, the reset mechanism uses the fixed m2(X) from the initial assume.    *   If z decreases (Case 3, i1 decreases), x is assigned __VERIFIER_nondet_int(). When i1 decreases, i2 is reset, and assume(i >= m2(X)) is enforced. Since x becomes non-deterministic but must satisfy x > 0, the minimum bound m2(X) must be 1.    *   If x decreases (Case 1, i2 decreases), no higher counter decreases or resets. i2 is decremented.    So, i2 maps to x, but its reset bound m2(X) must be 1.**Summary of the Lexicographical Tuple and Bounds:***   **i0 (Corresponds to y):** y always decreases or stays constant. m0(X) = y.*   **i1 (Corresponds to z):** z decreases (Case 3) or is havoc'd when i0 decreases (Case 2). When i1 is reset (due to i0 decreasing), z is assigned __VERIFIER_nondet_int(). Thus, m1(X) must be the minimum value z can take to ensure z > 0, which is 1.*   **i2 (Corresponds to x):** x decreases (Case 1) or is havoc'd when i1 decreases (Case 3). When i2 is reset (due to i0 or i1 decreasing), x might be assigned __VERIFIER_nondet_int() (Case 3). Thus, m2(X) must be the minimum value x can take to ensure x > 0, which is 1.The suitable lexicographical loop bound is (y, 1, 1).The output format requires a single assume statement with i0, i1, i2 bounds.assume(i >= y && i >= 1 && i >= 1);"
    #loop_bound, assume_stmts = extract_lexical_bounds(llm_answer)
    #print(f"Loop bound: {loop_bound}")
    #print(f"Assume statements: {assume_stmts}")
    #i_break_flag = False
    #for bound in loop_bound:
    #    pattern = r'\bi\b'
    #    if re.search(pattern, bound[1]):
    #        i_break_flag = True
    #        break
    #print(i_break_flag)
    k_file = '/tmpfs/tmp/K_aaron3_true-termination_true-valid-memsafety.bpl'
    insert_invariant(invariant, k_file)