#import genai
import openai
from openai import OpenAI, APIError
import time
#from google.genai import types
import requests
import json
import os

def type_explain(prompt_type, previous_llm_answer, ce, if_prompt_ce=True, if_prompt_hint=True):
    """Generate explanation for different verification failure types.

    Args:
        prompt_type: 1=grammar/format error, 2=verification fail (bound too small), 3=timeout
        previous_llm_answer: The previous LLM response that failed
        ce: Counterexample (only used when prompt_type==2)
        if_prompt_ce: Whether to include counterexample in feedback
        if_prompt_hint: Whether to include hints in feedback

    Returns:
        Explanation string for the failure type

    Raises:
        ValueError: If prompt_type is not 1, 2, or 3
    """
    if prompt_type == 1:  # grammar or format error
        if "Format error" in str(previous_llm_answer):
            return f"Your previous answer resulted in a format error: {previous_llm_answer}. \n"
        else:
            return f"Your previous answer {previous_llm_answer} contains a grammatical error. \n"
    elif prompt_type == 2:  # verification fail - loop bound too small
        specific_type_explain = f"Your previous answer {previous_llm_answer} is incorrect, \
which means the loop bound you provided is too small, and does not provide a sufficient upper bound on \
the number of loop iterations. \n"
        if if_prompt_ce:
            specific_type_explain = specific_type_explain + f"The following is a counterexample given by the verifier: {ce}. \n"
        elif not if_prompt_hint:
            specific_type_explain = f"Your previous answer {previous_llm_answer} can't be verified.\n"
        return specific_type_explain
    elif prompt_type == 3:  # verification timeout
        return f"Your previous answer {previous_llm_answer} resulted in verification issues, likely a timeout. \n"
    else:
        # This should never happen - prompt_type should always be 1, 2, or 3
        # Log a warning and return a generic message
        print(f"[Warning] Unexpected prompt_type={prompt_type} in type_explain, expected 1, 2, or 3")
        return f"Your previous answer {previous_llm_answer} could not be verified. \n"

def llmtype_message_map(prompt_type, previous_llm_answer, ce, repeat_notice, if_prompt_ce=True, if_prompt_hint=True):
    feed_back_content = ""
    specific_type_explain = type_explain(prompt_type, previous_llm_answer, ce if prompt_type == 2 else None, if_prompt_ce)
    
    if if_prompt_hint:
        # Full detailed feedback mode
        if prompt_type == 1: # grammar or format error
            if "Format error" in str(previous_llm_answer):
                feed_back_content = f"""
The output you provided did not follow the required format 'loop bound type: T, content: 'assume(...)'' exactly. 
Please ensure your next response follows this format strictly, providing both the type (0 or 1) and the content.
"""
            else:
                feed_back_content = f"""
When the verification of the program with the loop bound meets a  grammatical error, \
please modify the loop bound according to the following hints to overcome this problem. \
Please ensure that the expression is correctly formed with the \
loop counter on the left-hand side of the inequality sign (>=). \
Please pay special attention to the Notes below.\
Review the expression and correct any syntax errors before resubmitting.

**Notes:**
1. The expressions `m(X)` should generally be linear/affine functions of program variables `X`.\
***Avoid*** division ("/", "div") and non-linear functions like absolute value ("|x|", "abs").
2. The expressions `m(X)` should never contain a variable that is not \
declared in the Boogie code.
3. The loop counter(such as 'i', 'i0', 'i1') mustn't be show up on the right-hand side of the inequality.
    """
            if not repeat_notice:
                feed_back_content = specific_type_explain + feed_back_content
        if prompt_type == 2: #verificvation fail - loop bound too small
            feed_back_content = f"""
When the verification of the program with the loop bound meets a failure, \
please modify the loop bound according to the following hints to overcome this problem. \
Remember that the loop bound should be an overapproximation, meaning it can be \
larger than the actual number of iterations, but it must never be smaller. \
The bound must allow the verifier to prove that the implicit counter(s) \
eventually reach a non-positive state.
Please review the Boogie code and generate a new loop bound that satisfies \
the termination proof requirements.\
        """
            if not repeat_notice:
                feed_back_content = specific_type_explain + feed_back_content
        
        if prompt_type == 3: #verification time out - loop bound too large
            feed_back_content = f"""
When the verification of the program with the loop bound meets a timeout, \
please modify the loop bound according to the following hints to overcome this problem. \
This 'timeout' result could happen even if the loop bound is an overapproximation, if the verifier struggles to \
automatically infer the necessary loop **invariant(s)** that connect the loop bound counter(s) \
to the program variables and the loop's progress.
The previous loop bound might have been:
1.  Too complex, making invariant inference computationally expensive.
2.  Not tightly connected to the critical loop variables that determine termination, \
making it hard for the verifier to see how the bound decreases alongside the loop's progress.
We need a loop bound that provides a sufficient overapproximation but also **integrates better** \
with the loop's logic and variables. The bound expression(s) should reflect how the loop terminates \
and allow the verifier to more easily deduce an invariant that shows the counter(s) decrease \
towards zero as the loop progresses.
Please review the Boogie code and generate a new loop bound that addresses this by being \
both sufficiently large and well-connected to the loop's termination condition and variable updates.\
        """
            if not repeat_notice:
                feed_back_content = specific_type_explain + feed_back_content
    else:
        # Minimal feedback mode - only type explanation and simple instruction
        feed_back_content = f"""
Please review the Boogie code and generate a new loop bound based on the verification result.\
        """
        if not repeat_notice:
            feed_back_content = specific_type_explain + feed_back_content
    
    if not repeat_notice:
        common_note = """
***The answer you provide next must be different with your previous answer!***
**Just give your answer. Don't explain.**"""
        feed_back_content = feed_back_content + common_note
    
    return feed_back_content

def openai_gen_answer(boogie_code: str, prompt_type: int, message, repeat_notice=False, if_prompt_ce=True, if_prompt_hint=True) -> tuple:
    '''
    Generates an answer for loop bound inference.

    Returns:
        tuple: (result, infer_time, token_usage)
            - result: Content generated by LLM
            - infer_time: Inference time (seconds)
            - token_usage: dict containing {'prompt_tokens': int, 'completion_tokens': int, 'total_tokens': int}
    '''
    # LLM type 0: DeepSeek-V3.1-Terminus, type 1: gemini-2.5-flash
    # Default to DeepSeek (type 0)
    llm_type = 0
    if llm_type == 0:
        api_key = os.environ.get('DPSK_API_KEY')
        api_base = os.environ.get('DPSK_API_BASE')
    else:  # llm_type == 1
        api_key = os.environ.get('GEMINI_API_KEY')
        api_base = os.environ.get('GEMINI_API_BASE')
    [system_instruction, prompt_content] = generate_loop_bound_prompt(boogie_code, prompt_type, message, repeat_notice, if_prompt_ce, if_prompt_hint)
    client = OpenAI(
            api_key = api_key,
            base_url = api_base
        )
    while True:
        try:
            start_time = time.perf_counter()

            gptAnswer = client.chat.completions.create(
                messages=[
                    {'role': 'system', 'content': system_instruction},
                    {"role": "user", "content": prompt_content}],
                #timeout=120,
                #model = "gemini-2.5-flash",  # Replace with actual model name
                model = "DeepSeek-V3.1-Terminus",
                #model = "xdeepseekv31",
                extra_body={"thinking":{"type":"enabled"}},
                #extra_body={"enable_thinking":True},
                temperature=1.0
            )
            end_time = time.perf_counter()
            infer_time = end_time - start_time
            print(f"Inference time: {infer_time:.2f} seconds")
            # Process response...
            result = gptAnswer.choices[0].message.content.strip()
            # Extract token usage
            token_usage = {
                'prompt_tokens': getattr(gptAnswer.usage, 'prompt_tokens', 0) if gptAnswer.usage else 0,
                'completion_tokens': getattr(gptAnswer.usage, 'completion_tokens', 0) if gptAnswer.usage else 0,
                'total_tokens': getattr(gptAnswer.usage, 'total_tokens', 0) if gptAnswer.usage else 0
            }
            print(f"Token usage: prompt={token_usage['prompt_tokens']}, completion={token_usage['completion_tokens']}, total={token_usage['total_tokens']}")
            return (result, infer_time, token_usage)
        except APIError as e:
            print(f"OpenAI API error: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            time.sleep(5)

def generate_loop_bound_prompt(boogie_code: str, prompt_type: int, message, repeat_notice=False, if_prompt_ce=True, if_prompt_hint=True):
    """Generates a prompt for loop bound inference."""

    system_instruction = """
    You are an expert in formal verification and program analysis, specializing\\
    in termination proofs. Your task is to analyze the provided Boogie code and \\
    infer a suitable loop bound to help prove its termination.
    """

    system_instruction_lexical =  """
    You are an expert in formal verification and program analysis, specializing \
    in termination proofs for Boogie programs. Your task is to analyze the \
    provided Boogie code, determine the most appropriate type of loop bound \
    (Simple/Conjunctive or Lexical), and generate that loop bound in a specific \
    output format.
    """

    prompt_content = f"""
    **Context:**

    We are trying to prove the termination of a `while` loop in the following \\
    Boogie program. The program uses an implicit ranking function approach, \\
    where a counter variable `i` is decremented in each iteration.  The goal is \\
    to find a loop bound, represented by an expression in terms of the program \\
    variables, that provides an upper bound on the number of loop iterations. \\
    This loop bound will replace the placeholder `assume(%M:i%);`. 

    Loop Bound Description:

    The loop bound, denoted as m(X), should be an expression that represents the \\
    maximum number of iterations the while loop can execute before terminating, \\
    where 'X' represents the variables that can be shown in this expression.(etc. x,y...) \\
    The loop bound should be an overapproximation, meaning it can be larger than \\
    the actual number of iterations, but it must never be smaller. \\
    The loop bound is used in the precondition with an assume statement assume(i >= m(X));.\\
    For example: If X contain 2 variables: x and y, then the following assume statement\\
    can be generated: 'assume(i >= x + 10);', 'assume((i >= 1) && (i >= y));'.

    **Task:**

    Based on the provided Boogie code and the reasoning points, generate a \\
    suitable loop bound to replace the 'assume(%M:i%);' statement. Provide the \\
    loop bound in terms of X. 

    **Notes:**

    1. The generated loop bound should consist of one or more assume expressions.\\
    Each expression should contain an inequality involving the loop counter 'i' \\
    and a greater-or-equal-than sign (>=), with 'i' positioned on the left-hand side of the inequality.
    2. Conjunction (&&) is permitted between the predicates inside the assume expression, \\
    but disjunction (||) is not allowed even to appear.
    3. If more than one assume expressions are needed, separate them with a comma (;).\\
    For example: 'assume(i >= x + 10); assume(i >= y);'. Even if there is only one expression, \\
    a comma is still needed at the end of the expression.
    4. The generated loop bound expression should not contain division symbols such as "/"\\
    or "div," nor should it include nonlinear expressions, such as "|x|" or "abs." Otherwise,\\
    a syntax error will occur during verification.

    **Boogie Code:**

    ```boogie
    {boogie_code}

    **Output:**
    Replace the placeholder with the inferred loop bound condition, \\
    using conjunctions of inequalities as described above.\\
    Just provide the loop bound condition, not the full Boogie code.\\
    Don't explain.
    """

    prompt_content_lexical = f"""
    **Context:**

    We are trying to prove the termination of a `while` loop in the following \
    Boogie program. The goal is to find a loop bound expression that provides \
    an upper bound on the number of loop iterations. The generated `assume` \
    statement will be placed before the loop. The type of loop bound determines \
    how termination counters are implicitly managed during verification.

    Loop Bound Types, Verification Logic, and Generation Formats:

    1.  **Simple/Conjunctive Loop Bound (Output Type 0):**
        *   **Meaning:** Bounds the loop based on a single measure of progress.
        *   **Verification Logic:** During verification, a single implicit counter\
            `i` is assumed to exist. This counter `i` is initialized to be greater \
            than or equal to the bound expression(s) before the loop, and is **decremented by 1**\
            in each loop iteration. An assertion `assert(i >= 0);` is implicitly checked within the loop.
        *   **Generated Format:** `assume(i >= m1(X) && i >= m2(X) && ...);` where `m1, m2, ...`\
            are expressions in terms of program variables `X`. Multiple bounds on `i` imply `i` is\
            bounded by their maximum.

    2.  **Lexical Loop Bound (Output Type 1):**
        *   **Meaning:** Bounds the loop based on a prioritized, multi-dimensional \
            measure of progress. Suitable for nested loops or complex control flow \
            where termination depends on multiple factors decreasing in order.
        *   **Verification Logic:** During verification, multiple implicit counters \
            `i0, i1, ..., ik` (currently **up to k=2**, i.e., `i0, i1, i2`) are assumed. \
            These counters are initialized according to the generated `assume` bounds. \
            The **decrement logic** applied *at the end of each iteration* ensures lexicographical decrease:
            ```
            // Example for k=1 (counters i0, i1)
            if (i1 > 0) {{
              i1 := i1 - 1;
            }} else {{
              i0 := i0 - 1;
              havoc i1; // Reset i1
              assume(i1 >= bound_for_i1(X)); // Re-assume its bound
            }}
            // Assertion implicitly checks i0 >= 0 (and potentially others depending on tool)
            ```
            This logic prioritizes decrementing the *last* counter (`ik`). Only if it's already\
            non-positive does it attempt to decrement the previous counter (`i(k-1)`) and \
            reset the subsequent ones (`ik`, etc.).
        *   **Generated Format:** `assume(i0 >= m0(X) && i1 >= m1(X) && ... && ik >= mk(X));`\
            where `m0, m1, ..., mk` are expressions for each counter. All bounds *must* be\
            combined using `&&` in a single `assume`.

    General Loop Bound Properties:
    *   The loop bound should be an overapproximation (never smaller than actual iterations).
    *   The expressions `m(X)` should generally be linear/affine functions of program variables `X`.\
        Avoid division ("/", "div") and non-linear functions like absolute value ("|x|", "abs").

    **Task:**

    1.  Analyze the structure, variable updates, and control flow within the `while` loop\
        in the provided Boogie code.
    2.  Determine the most suitable type of loop bound: Simple/Conjunctive (Type 0) or Lexical (Type 1).\
        Consider Lexical (Type 1) if termination clearly depends on multiple variables decreasing \
        in a prioritized, lexicographical manner (check examples in Lexical description). Otherwise,\
        default to Simple/Conjunctive (Type 0).
    3.  Generate the chosen loop bound *exactly* in the specified output format below.

    **Boogie Code:**

    ```boogie
    {boogie_code}
    ```

    **Output Format:**

    Provide the output *exactly* in the following format on a single line:
    `loop bound type: T, content: 'assume(...)'`

    *   Replace `T` with `0` for Simple/Conjunctive or `1` for Lexical.
    *   Replace `assume(...)` with the generated assume statement containing the complete bound condition(s).\
        Use `&&` to combine multiple predicates within the single `assume` statement.
    *   Do **not** add any other text, explanation, code, or formatting.

    **Example Outputs:**
    `loop bound type: 0, content: 'assume(i >= x && i >= y);'`
    `loop bound type: 1, content: 'assume(i0 >= x + 2 && i1 >= 10);'`

    **Notes:**
    1. The generated loop bound content should consist of one or more assume expressions.\\
    Each expression should contain an inequality involving the loop counter 'i' or 'i0'/'i1'/'i2' \\
    and a greater-or-equal-than sign (>=), with loop counter positioned on the left-hand side of the inequality.
    2. Conjunction (&&) is permitted between the predicates inside the assume expression, \\
    but disjunction (||) is not allowed even to appear.
    3. If more than one assume expressions are needed when loop bound type is 0, separate them with a comma (;).\\
    For example: 'assume(i >= x + 10); assume(i >= y);'.
    4. The generated loop bound expression should not contain division symbols such as "/"\\
    or "div," nor should it include nonlinear expressions, such as "|x|" or "abs." Otherwise,\\
    a syntax error will occur during verification.
    5. The loop counter mustn't show up on the right-hand side of the inequality.
    """

    feed_back_content = ""
    
    if not repeat_notice and prompt_type != 0:
        # Single previous answer feedback
        if isinstance(message, list):
            prev_ans = message[0] if len(message) > 0 else ""
            ce = message[2] if len(message) > 2 else None
        else:
            prev_ans = message
            ce = None
        feed_back_content = llmtype_message_map(prompt_type, prev_ans, ce, repeat_notice, if_prompt_ce, if_prompt_hint)
    elif repeat_notice:
        # Multiple history feedback
        prev_prompt_type = []
        initial_feed_back = "Now I will inform you of the loop bounds you once provided along with the types of \
problems found during their verification. Please analyze these information and the hints attached to \
them, and then generate a valid loop bound anew."
        partially_feedback = ""
        type_explain_mess = ""

        # message should be [previous_llm_answers, prompt_types, ces]
        # Validate structure: list of length 3, where each element is also a list
        if (isinstance(message, list) and len(message) == 3 and
            all(isinstance(item, list) for item in message)):
            previous_llm_answers = message[0]
            prompt_types = message[1]
            ces = message[2]
        else:
            # Fallback: if message structure is incorrect, skip history feedback
            print(f"[Warning] Invalid message structure for repeat_notice mode: {type(message)}, len={len(message) if isinstance(message, list) else 'N/A'}")
            if isinstance(message, list) and len(message) == 3:
                print(f"  message[0] type: {type(message[0])}, message[1] type: {type(message[1])}, message[2] type: {type(message[2])}")
            # Return without history feedback
            previous_llm_answers = []
            prompt_types = []
            ces = []

        for i, prev_loop_bound in enumerate(previous_llm_answers):
            # prompt_types and ces should have the same length as previous_llm_answers
            # If not, skip this entry to avoid errors
            if i >= len(prompt_types):
                print(f"[Warning] prompt_types shorter than previous_llm_answers at index {i}")
                continue
            current_type = prompt_types[i]
            # Validate that current_type is a valid value (1, 2, or 3)
            if current_type not in (1, 2, 3):
                print(f"[Warning] Invalid prompt_type={current_type} at index {i}, skipping")
                continue
            current_ce = ces[i] if i < len(ces) and current_type == 2 else None
            type_explain_mess += '\n' + type_explain(current_type, prev_loop_bound, current_ce, if_prompt_ce)
            if current_type not in prev_prompt_type:
                partially_feedback += '\n' + llmtype_message_map(current_type, None, current_ce, repeat_notice, if_prompt_ce, if_prompt_hint)
                prev_prompt_type.append(current_type)
        
        common_note = """
***The answer you provide next must be different with your previous answers!***
**Just give your answer. Don't explain.**"""
        partially_feedback = partially_feedback + "\n" + common_note
        feed_back_content = initial_feed_back + type_explain_mess + partially_feedback
    
    # Old single message feedback logic (backward compatibility)
    prev_ans = message if isinstance(message, str) else (message[0] if isinstance(message, list) and len(message) > 0 else "")
    if prompt_type == 1 and not repeat_notice and not feed_back_content: #ice error (grammar error)
        pass  # Already handled above
    
    #prompt_content = prompt_content + feed_back_content
    #return [system_instruction, prompt_content]
    prompt_content_lexical = prompt_content_lexical + feed_back_content
    return [system_instruction_lexical, prompt_content_lexical]

if __name__ == "__main__":
    boogie_code = """
    function {:existential true} b0(x:int, y:int, z:int, i:int %Decl:i%): bool;
    procedure main()
    {
    var x,y,z,i: int;

    havoc x;
    y := 100;
    z := 1;

    assume(%M:i%);
        
    while (x >= 0)
    invariant b0(x,y,z,i %Inv:i%);
    {
        assert(i > 0);
        x := x - y;
        y := y - z;
        z := -z;
        
        i := i - 1;
    }
    }

    """
    answer = openai_gen_answer(boogie_code, 0, [])
    print(answer)
