#import genai
import os
import openai
from openai import OpenAI, APIError
import time
import requests
import json
#from google.genai import types

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
    """
    if prompt_type == 1:  # ice error (grammar error)
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
        # Log a warning and return a generic message to avoid UnboundLocalError
        print(f"[Warning] Unexpected prompt_type={prompt_type} in type_explain, expected 1, 2, or 3")
        return f"Your previous answer {previous_llm_answer} could not be verified. \n"

def llmtype_message_map(prompt_type, previous_llm_answer, ce, repeat_notice, if_prompt_ce=True, if_prompt_hint=True):
    feed_back_content = ""
    specific_type_explain = type_explain(prompt_type, previous_llm_answer, ce if prompt_type == 2 else None, if_prompt_ce)
    
    if if_prompt_hint:
        # Full detailed feedback mode
        if prompt_type == 1: #ice error (grammar error)
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
        
        if prompt_type == 3: #verification time out
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

def openai_gen_answer(gen_type, llm_type, boogie_code: str, conj_or_lex, prompt_type, previous_llm_answer, ce, repeat_notice = False, code_type = 'Boogie', if_prompt_ce=True, if_prompt_hint=True) -> tuple:
    '''
    llm_type indicates different large language models:
    0 - DeepSeek-V3.1-Terminus
    1 - gemini-2.5-flash
    
    Returns:
        tuple: (result, infer_time, token_usage)
            - result: Content generated by LLM
            - infer_time: Inference time (seconds)
            - token_usage: dict containing {'prompt_tokens': int, 'completion_tokens': int, 'total_tokens': int}
    '''
    if gen_type == 0:
        [system_instruction, prompt_content] = generate_loop_bound_prompt(boogie_code, conj_or_lex, prompt_type, previous_llm_answer, ce, repeat_notice, code_type, if_prompt_ce, if_prompt_hint)
    elif gen_type == 1:
        [system_instruction, prompt_content] = generate_loop_invariant_prompt(boogie_code, prompt_type, previous_llm_answer, ce, repeat_notice)
    max_retries = 8
    if llm_type == 0:
        # DeepSeek-V3.1-Terminus
        api_key = os.environ.get('DPSK_API_KEY')
        api_base = os.environ.get('DPSK_API_BASE')
        llm_name = "DeepSeek-V3.1-Terminus"
        client = OpenAI(
        api_key = api_key,
        base_url = api_base
    )  # Create OpenAI client instance
        while True:
            try:
                start_time = time.perf_counter()
                gptAnswer = client.chat.completions.create(
                    messages=[
                        {'role': 'system', 'content': system_instruction},
                        {"role": "user", "content": prompt_content}],
                    #extra_body = {"chat_template_kwargs": {"thinking": True}},
                    #extra_body={"thinking":{"type":"enabled"}},
                    #timeout=120,  # Increase timeout
                    max_tokens = 30000,
                    model = llm_name,  # Replace with actual model name
                    temperature=1.0
                )
                end_time = time.perf_counter()
                infer_time = end_time - start_time
                print(f"Inference time: {infer_time:.2f} seconds")
                # Process response...
                result = gptAnswer.choices[0].message.content.strip()  # Get generated content and strip whitespace
                # Extract token usage
                token_usage = {
                    'prompt_tokens': getattr(gptAnswer.usage, 'prompt_tokens', 0) if gptAnswer.usage else 0,
                    'completion_tokens': getattr(gptAnswer.usage, 'completion_tokens', 0) if gptAnswer.usage else 0,
                    'total_tokens': getattr(gptAnswer.usage, 'total_tokens', 0) if gptAnswer.usage else 0
                }
                print(f"Token usage: prompt={token_usage['prompt_tokens']}, completion={token_usage['completion_tokens']}, total={token_usage['total_tokens']}")
                return (result, infer_time, token_usage)  # Return generated content, inference time and token usage
            except APIError as e:
                print(f"OpenAI API error: {e}")
                time.sleep(5)
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                time.sleep(5)
    elif llm_type == 1:
        # gemini-2.5-flash
        api_key = os.environ.get('GEMINI_API_KEY')
        api_base = os.environ.get('GEMINI_API_BASE')
        model_name = "gemini-2.5-flash"
        for attempt in range(max_retries):
            client = OpenAI(
                api_key = api_key,
                base_url = api_base
            )
            try:
                start_time = time.perf_counter()
                gptAnswer = client.chat.completions.create(
                    messages=[
                        {'role': 'system', 'content': system_instruction},
                        {"role": "user", "content": prompt_content}],
                    #timeout=120, 
                    model = model_name,
                    #model = "google/gemini-3-flash-preview"
                )
                end_time = time.perf_counter()
                infer_time = end_time - start_time
                print(f"Inference time: {infer_time:.2f} seconds")
                # Process response...
                result = gptAnswer.choices[0].message.content.strip()  # Get generated content and strip whitespace
                # Extract token usage
                token_usage = {
                    'prompt_tokens': getattr(gptAnswer.usage, 'prompt_tokens', 0) if gptAnswer.usage else 0,
                    'completion_tokens': getattr(gptAnswer.usage, 'completion_tokens', 0) if gptAnswer.usage else 0,
                    'total_tokens': getattr(gptAnswer.usage, 'total_tokens', 0) if gptAnswer.usage else 0
                }
                print(f"Token usage: prompt={token_usage['prompt_tokens']}, completion={token_usage['completion_tokens']}, total={token_usage['total_tokens']}")
                return (result, infer_time, token_usage)  # Return generated content, inference time and token usage
            except APIError as e:
                print(f"OpenAI API error: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    print("All attempts failed, returning default value")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                if attempt < max_retries - 1:
                    time.sleep(5)
                else:
                    print("All attempts failed, returning default value")
        

def generate_loop_bound_prompt(boogie_code: str, conj_or_lex, prompt_type, previous_llm_answer, ce, repeat_notice = False, code_type = 'Boogie', if_prompt_ce=True, if_prompt_hint=True):
    """Generates a prompt for loop bound inference."""
    system_instruction_conj = """
    You are an expert in formal verification and program analysis, specializing\
    in termination proofs. Your task is to analyze the provided {code_type} code and \
    infer a suitable loop bound to help prove its termination.
    """

    prompt_content_conj = f"""
    **Context:**

We are trying to prove the termination of a `while` loop in the following \
Boogie program. The program uses an implicit ranking function approach, \
where a counter variable `i` is decremented in each iteration.  The goal is \
to find a loop bound, represented by an expression in terms of the program \
variables, that provides an upper bound on the number of loop iterations. \
This loop bound will replace the placeholder `assume(%M:i%);`. 

Loop Bound Description:

The loop bound, denoted as m(X), should be an expression that represents the \
maximum number of iterations the while loop can execute before terminating, \
where 'X' represents the variables that can be shown in this expression.(etc. x,y...) \
The loop bound should be an overapproximation, meaning it can be larger than \
the actual number of iterations, but it must never be smaller. \
The loop bound is used in the precondition with an assume statement assume(i >= m(X));.\
For example: If X contain 2 variables: x and y, then the following assume statement\
can be generated: 'assume(i >= x + 10);', 'assume((i >= 1) && (i >= y));'.

**Task:**

Based on the provided Boogie code and the reasoning points, generate a \
suitable loop bound to replace the 'assume(%M:i%);' statement. Provide the \
loop bound in terms of X. 

**Notes:**

1. The generated loop bound should consist of one or more assume expressions.\
Each expression should contain an inequality involving the loop counter 'i' \
and a greater-or-equal-than sign (>=), with 'i' positioned on the left-hand side of the inequality.
2. The loop counter 'i' mustn't be show up on the right-hand side of the inequality.
3. Conjunction (&&) is permitted between the predicates inside the assume expression, \
but disjunction (||) is not allowed even to appear.
4. If more than one assume expressions are needed, separate them with a comma (;).\
For example: 'assume(i >= x + 10); assume(i >= y);'. Note the semicolon (;) at the \
end of each assume expression ** including the last one **.
5. The generated loop bound expression should not contain division symbols such as "/"\
or "div," nor should it include nonlinear expressions, such as "|x|" or "abs." Otherwise,\
a syntax error will occur during verification.

    **{code_type} Code:**

    ```{code_type}
    {boogie_code}

**Output:**
Replace the placeholder with the inferred loop bound condition, \
using conjunctions of inequalities as described above.\
Just provide the loop bound condition, not the full Boogie code.\
Don't explain.
    """

    system_instruction_lexical =  """
You are an expert in formal verification and program analysis, specializing \
in termination proofs for {code_type} programs, particularly skilled at identifying \
lexicographical ranking functions and loop bounds. Your task is to analyze the \
provided {code_type} code and generate a suitable lexicographical loop bound \
to help prove its termination, following a specific format.
    """

    prompt_content_lexical = f"""
    **Context:**

We are trying to prove the termination of a `while` loop in the following \
{code_type} program. The goal is to find a loop bound expression that provides \
an upper bound on the number of loop iterations.

In previous attempts, we have explored generating simple or conjunctive loop bounds, \
but these have not been sufficient to prove termination for this specific loop. \
We now need to consider a more advanced technique: **Lexicographical Loop Bounds**.

Lexicographical Loop Bounds Explained:

Lexicographical termination relies on a sequence of expressions (a tuple), where \
each loop iteration decreases this tuple with respect to a lexicographical order. \
This means the *last* element in the tuple must decrease, and if it becomes non-positive, \
the *previous* element must decrease, and the last element is reset to a non-negative value (determined by its bound).

During verification, this is modeled using multiple implicit counters: `i0, i1, ..., ik` \
(currently supported up to k=2, i.e., `i0, i1, i2`). The generated `assume` statement \
placed before the loop provides the initial bounds for these counters. The implicit decrement \
logic applied *at the end of each iteration* simulates the lexicographical decrease. For a tuple (i0, i1, i2):
```
// Example decrement logic (simplified)
if (i2 > 0) {{
    i2 := i2 - 1;
}} else if (i1 > 0) {{
    i1 := i1 - 1;
    havoc i2; assume(i2 >= m2(X)); // Reset i2
}} else {{
    i0 := i0 - 1;
    havoc i1, i2; assume(i1 >= m1(X)); assume(i2 >= m2(X)); // Reset i1, i2
}}
// Assertion implicitly checks i0 >= 0 (and potentially others)
```
The system attempts to decrement the last counter. Only if it's non-positive does it move to the previous counter,\
decrement it, and reset the subsequent ones based on their bounds. Termination is proven if `i0` eventually reaches\
a non-positive value while all subsequent counters satisfy their bounds.

General Loop Bound Properties:
*   The loop bound should be an overapproximation (never smaller than actual iterations).
*   The expressions `m(X)` should generally be linear/affine functions of program variables `X`.\
    Avoid division ("/", "div") and non-linear functions like absolute value ("|x|", "abs").

    **Task:**

Analyze the structure, variable updates, and control flow within the `while` loop\
in the provided {code_type} code to infer a suitable **Lexicographical Loop Bound**. \
Determine the necessary counters (`i0`, `i1`, etc., up to `i2`) and their corresponding bounds \
in terms of the program variables `X`.

    **{code_type} Code:**

    ```
    {boogie_code}
    ```

    **Output Format:**

Provide the output *exactly* in the following format on a single line:
'assume(i0 >= m0(X) && i1 >= m1(X) && ...);'

*   The content must be a single `assume` statement containing bounds for `i0`, `i1`, etc., combined using `&&`.
*   Do **not** include any other text, explanation, code, or formatting.
*   The loop counter (such as 'i', 'i0', 'i1') mustn't show up on the right-hand side of the inequality.

**Example Output:**
'assume(i0 >= x + y && i1 >= y);'
'assume(i0 >= 10 && i1 >= z + 5 && i2 >= 0);'
    """
    feed_back_content = ""

    if not repeat_notice and prompt_type != 0:
        feed_back_content = llmtype_message_map(prompt_type, previous_llm_answer, ce, repeat_notice, if_prompt_ce, if_prompt_hint)

    elif repeat_notice:
        prev_prompt_type = []
        initial_feed_back = "Now I will inform you of the loop bounds you once provided along with the types of \
problems found during their verification. Please analyze these information and the hints attached to \
them, and then generate a valid loop bound anew."
        partially_feedback = ""
        type_explain_mess = ""
        for i, prev_loop_bound in enumerate(previous_llm_answer):
            current_type = prompt_type[i]
            current_ce = None
            if current_type == 2:
                current_ce = ce[i]
            type_explain_mess += '\n' + type_explain(current_type, prev_loop_bound, current_ce, if_prompt_ce)
            if not current_type in prev_prompt_type:
                partially_feedback += '\n' + llmtype_message_map(current_type, None, current_ce, repeat_notice, if_prompt_ce, if_prompt_hint)
                prev_prompt_type.append(current_type)
        common_note = """
***The answer you provide next must be different with your previous answers!***
**Just give your answer. Don't explain.**"""
        partially_feedback = partially_feedback + "\n" + common_note
        feed_back_content = initial_feed_back + type_explain_mess + partially_feedback

    if conj_or_lex == False:
        system_instruction = system_instruction_conj
        prompt_content = prompt_content_conj
    else:
        system_instruction = system_instruction_lexical
        prompt_content = prompt_content_lexical

    #prompt_content = prompt_content + feed_back_content
    #return [system_instruction, prompt_content]
    prompt_content = prompt_content + feed_back_content
    return [system_instruction, prompt_content]

def generate_loop_invariant_prompt(code: str, prompt_type, previous_llm_answer, ces, repeat_notice = False):
    system_instruction = f"""
You are an expert in software verification and program logic. Your task is to analyze a
Boogie procedure and synthesize a suitable loop invariant. The primary purpose of this
invariant is to be strong enough to formally prove that an `assert` statement inside
the loop body always holds true.
    """

    prompt_content = f"""
    **Context:**

We need to formally verify the correctness of the `assert` statement within the `while`
loop of the following Boogie procedure. To do this, we must discover a **Loop Invariant**.

A Loop Invariant is a logical property that holds true at three key points:
1.  **Before the loop starts (Initiation):** The properties established by the pre-loop
    `assume` statements must be sufficient to prove the invariant is true initially.
2.  **At the start of every iteration (Preservation):** If we assume the invariant and the
    loop condition are true, then after executing the loop body once, the invariant
    must remain true.
3.  **To prove the assertion (Sufficiency):** The invariant, combined with the loop
    condition, must be strong enough to logically imply that the `assert` statement
    inside the loop is always true.
    
    **Task:**

Analyze the Boogie procedure below. Your goal is to generate a loop invariant that satisfies
all three properties described above, with a special focus on making the `assert(i > 0);`
provable.

    **Boogie Code:**
    ```Boogie
    {code}
    ```

    **Output Format Requirements:**

    Your output must be a single line in the format: `invariant [EXPRESSION];`
    - `EXPRESSION` is the synthesized invariant.
    - Use `&&` and `||` within `EXPRESSION` to combine predicates for a complex invariant.
    - Always parenthesize when mixing disjunction and conjunction: Boogie gives && higher precedence than ||. To avoid parse ambiguity, group explicitly:
        Bad: invariant (A || B && C);
        Good: invariant ((A) || ((B) && (C)));
    - The output must start with the keyword `invariant` and end with a semicolon `;`.
    - The entire invariant, including all its predicates, must be encapsulated within a single `invariant [...];` statement.
    - The invariant expression EXPRESSION must be ### contained in a pair of square brackets formed as [EXPRESSION] ### !!!
    - The invariant expression must be syntactically valid in Boogie and must not include non-standard functions (like "|x|", "abs").
    - Do not explain.
    """
    feed_back_content = f"Your previous answer {previous_llm_answer} "
    for index, type in enumerate(prompt_type):
        if len(ces) and type != 2:
            ce = ces[index]
        if index > 0:
            feed_back_content += f"\n In addition, Your previous answer {previous_llm_answer} also "

        if type == 0: # Verification timeout
            feed_back_content += f"""
resulted in verification issues, likely a timeout. \
This can happen even if the invariant is correct, if it is too complex or not sufficiently connected \
to the loop's logic and variables. We need an invariant that is both strong enough to prove the assertion \
and also allows the verifier to efficiently check the initiation and preservation conditions.

Please review the Boogie code and generate a new loop invariant that addresses this by being \
both sufficiently strong and well-connected to the loop's condition and variable updates.\
        """
        if type == 2: # Grammar error
            feed_back_content += f"""
contains a grammatical error or can not be extracted correctly. \
Please ensure that the expression is correctly formed and follows the output format requirements. \
Pay special attention to the Notes below. Review the expression and correct any syntax errors before resubmitting.

**Notes:**
1. The invariant expression EXPRESSION must be ### contained in a pair of square brackets formed as [EXPRESSION] ### !!!
2. The output must start with the keyword `invariant` and end with a semicolon `;`.
3. The entire invariant, including all its predicates, must be encapsulated within a single `invariant [...];` statement.
4. Always parenthesize when mixing disjunction and conjunction: Boogie gives && higher precedence than ||. To avoid parse ambiguity, group explicitly:
        Bad: invariant (A || B && C);
        Good: invariant ((A) || ((B) && (C)));
5. Use `&&` and `||` within `EXPRESSION` to combine predicates for a complex invariant.
6. The invariant expression must be syntactically valid in Boogie and must not include non-standard functions (like "|x|", "abs").
7. ***The answer you provide next must be different with your previous answer!***
            """
        if type == 3: # Reachability fail
            feed_back_content += "'is too strict and not reachable. \
The Reachability of the loop invariant means that the loop invariant I can be derived based on the pre-condition P, i.e. P ⇒ I. \
The following is a counterexample given by the verifier: "+ ce + ". \
In order to get a correct answer, You may want to consider the initial situation where the program won't enter the loop. \
Use '&&' or '||' if necessary."
            
        if type == 4: # Inductiveness fail
            feed_back_content += "'is not inductive. \
The Inductive of the loop invariant means that if the program state satisfies loop condition B, the new state obtained after the loop execution S still satisfies, i.e. {I ∧ B} S {I}. \
The following is a counterexample given by the verifier: "+ ce + ". \
In order to get a correct answer, You may want to consider the special case of the program executing to the end of the loop. \
Use '&&' or '||' if necessary."

        if type == 5: # Constraint too weak, assert fails
            feed_back_content += "'is too weak and not provable. \
The Provability of the loop invariant means that after unsatisfying loop condition B, we can prove the assertion Q (Q is 'assert(i > 0);' in our case), i.e. (I ∧ ¬ B) ⇒ Q. \
The following is a counterexample given by the verifier: "+ ce + ". \
In order to get a correct answer, you may want to consider the special case of the program executing to the end of the loop. If some of the preconditions are also loop invariant, you need to add them to your answer as well. \
Use '&&' or '||' if necessary."

    feed_back_content += "***The answer you provide next must be different with your previous answer!*** **Just give your answer. Don't explain.**"
    if len(prompt_type):
        prompt_content = prompt_content + feed_back_content
    if repeat_notice:  
        prompt_content = prompt_content + f"\n**# Your previous answer {previous_llm_answer} has already been tried and resulted in verification issues so many times. Please provide a different answer this time.***"
    return [system_instruction, prompt_content]


if __name__ == "__main__":
    boogie_code = """
    procedure main()
    {
    var c,x,i: int;

    havoc c;
    havoc x;

    assume(c >= 10);
    assume(i >= 1 && i >= x + c + 1);
    while (x + c >= 0)
    {
        assert(i > 0);
        x := x - c;
        c := c + 1;
        i := i - 1;
    }
    }

    """
    gen_type = 0
    llm_type = 6
    conj_or_lex = 0
    prompt_type = [1, 2, 3]
    previous_llm_answer = ['assume i >= i;', 'assume i >= 1;', 'assume i >= x + c']
    ce = [None, 'example_ce1', None]
    repeat_notice = True
    #answer = openai_gen_answer(1, 0, boogie_code, 0, [0], '', ['1'])
    answer = openai_gen_answer(gen_type, llm_type, boogie_code, conj_or_lex, prompt_type, previous_llm_answer, ce, repeat_notice)
    print(answer)
