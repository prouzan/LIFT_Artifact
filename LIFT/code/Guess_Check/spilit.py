import re

def find_outer_operator(expression):
    """
    Find the outermost logical operator (&& or ||) in an expression.
    According to C language precedence, '||' has lower precedence than '&&', so the outermost separator should be '||'.
    """
    bracket_count = 0
    # First check if there's a top-level '||'
    for i, char in enumerate(expression):
        if char == '(':
            bracket_count += 1
        elif char == ')':
            bracket_count -= 1
        elif bracket_count == 0 and expression[i:i+2] == '||':
            return '||'
    
    # If no top-level '||', check for top-level '&&'
    bracket_count = 0 # Reset counter
    for i, char in enumerate(expression):
        if char == '(':
            bracket_count += 1
        elif char == ')':
            bracket_count -= 1
        elif bracket_count == 0 and expression[i:i+2] == '&&':
            return '&&'
            
    return None

def split_expression_by_operator(expression, operator):
    """
    Split expression by given top-level operator, ignoring operators inside parentheses.
    """
    parts = []
    bracket_count = 0
    start_index = 0
    op_len = len(operator)

    for i, char in enumerate(expression):
        if char == '(':
            bracket_count += 1
        elif char == ')':
            bracket_count -= 1
        # When not inside any parentheses and encountering target operator
        elif bracket_count == 0 and expression[i:i+op_len] == operator:
            parts.append(expression[start_index:i].strip())
            start_index = i + op_len
            
    # Add the last (or only) predicate
    parts.append(expression[start_index:].strip())
    return parts

def split_invariant_predicates(invariant_statement):
    """
    Extract and split predicates from 'invariant(...);' statement.
    """
    # Use regex to extract content inside parentheses
    match = re.search(r'invariant\s*\((.*)\)\s*;', invariant_statement)
    if not match:
        return [], None
    
    expression = match.group(1).strip()
    
    # Find the outermost operator
    outer_operator = find_outer_operator(expression)
    
    # If top-level operator found, use it to split expression
    if outer_operator:
        predicates = split_expression_by_operator(expression, outer_operator)
    # Otherwise, the entire expression is a single predicate
    else:
        predicates = [expression]
        
    return predicates, outer_operator


if __name__ == "__main__":
    # Test with new 'invariant' statements
    test_cases = [
        "invariant((x >= -50) && (y >= 0) && (y == 0 && x + y >= -49));",
        "invariant((x >= -50) || (y >= 0) || (y == 0 && x + y >= -49));",
        "invariant(x >= -50 && y >= 0 && y == 0 || (x + y >= -49 && x > 100));",
        "invariant((lock == 0 && x != y) || (lock == 1 && x == y));",
        "invariant((j == (i * (i - 1)) / 2) && (i >= 0) && (i <= n) && (k >= 0));",
        "invariant((x >= y) && (y <= 100000));",
        "invariant(y <= 100000);",
        "invariant(x >= y && y <= 100000);",
        "invariant((x == y + 10*n) && (x >= 0) || (x == 0 && y == 0));",
        "invariant((n>0&&x<0) || (n>0&&x>=0) || (n<=0&&x<=0));"
    ]

    for test in test_cases:
        print(f"Input: {test}")
        predicates, operator = split_invariant_predicates(test)
        print(f"  -> Predicates: {predicates}")
        print(f"  -> Operator: '{operator}'")
        print("-" * 50)