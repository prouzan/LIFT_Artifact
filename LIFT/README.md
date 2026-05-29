# LIFT: LLM-Guided Loop Bound Generation for Termination Verification

The core implementation is in `code/Guess_Check/`. It implements the **LIFT** framework, an LLM-guided approach for program termination verification through loop bound generation and validation.

## Overview

LIFT leverages Large Language Models (LLMs) to generate loop bounds that serve as termination witnesses for program verification. The framework implements a **guess-and-check** methodology with **diagnostic feedback** to iteratively refine loop bound candidates until successful verification or resource exhaustion.

### Key Features

- **Progressive Loop Bound Generation**: Starts with conjunctive bounds for single-loop programs, then escalates to lexicographic bounds for complex cases
- **Guess-and-Check Verification**: Uses LLM to "guess" loop bounds and ICE-DT to "check" via invariant inference
- **Counterexample-Guided Refinement**: Provides diagnostic feedback from verification failures to guide LLM improvements
- **Multiple LLM Support**: Supports DeepSeek-V3.1-Terminus and Gemini-2.5-flash
- **Multiple Invariant Inference Paths**: Supports ICE-DT (default), a LIFT-compatible Lam4Inv reproduction, and Lemur
- **Batch Processing**: Supports processing multiple benchmark files through `config.yaml`

## Architecture

```
Guess_Check/
├── Check_loop_bound_newiter.py       # Main experiment: Gemini/DeepSeek for guess + ICE-DT for check
├── Check_loop_bound_lam4inv.py       # Alternative: self-reproduced Lam4Inv invariant inference path
├── Check_loop_bound_lemur.py         # Alternative: Uses Lemur for invariant inference
├── Check_loop_bound_llmselfchoice.py # Unified strategy experiment (RQ3 Part 1)
├── CBC_Transform.py                  # Bounded checking transformation
├── K_Transform.py                    # K-induction Boogie transformation
├── ReInvariantChecker.py             # Failure diagnosis for invariant/loop-bound checks
├── DataInfo.py                       # Benchmark metadata
├── config.yaml                       # Configuration file
├── prompt_gen_newiter.py             # LLM prompt generation (progressive strategy)
├── prompt_gen_llmselfchoice.py       # LLM prompt generation (unified strategy)
├── spilit.py                         # Invariant predicate splitting helpers
└── utils.py                          # Parsing, logging, Boogie, and result utilities
```

### `Guess_Check` File Roles

#### Main Experiment Path

- **`Check_loop_bound_newiter.py`**: Primary LIFT experiment driver for RQ1/RQ2. It coordinates progressive loop-bound generation, constant-bound and const-added attempts, K-induction verification, ICE-DT/Boogie invocation, result parsing, and diagnostic feedback across iterations.
- **`CBC_Transform.py`**: Generates bounded Boogie programs for constant-bound checks and const-added validation attempts.
- **`K_Transform.py`**: Builds the K-induction Boogie programs used to check candidate loop bounds, including the lexicographic-bound variant.
- **`ReInvariantChecker.py`**: Analyzes failed verification output to help distinguish loop-bound failures from invariant failures and to provide feedback for later attempts.
- **`prompt_gen_newiter.py`**: Builds prompts for the progressive LIFT strategy, including feedback prompts after failed checks.
- **`utils.py`**: Provides shared parsing and result-handling utilities for LLM outputs, Boogie/ICE-DT output, counterexamples, invariants, and generated files.
- **`config.yaml`** and **`DataInfo.py`**: Store experiment configuration and benchmark metadata used by the main driver.

#### Comparison and Ablation Scripts

- **`Check_loop_bound_llmselfchoice.py`**: Unified-strategy driver for RQ3 Part 1. Instead of forcing the progressive conjunctive-then-lexicographic order, it lets the LLM choose the loop-bound form in a single strategy.
- **`Check_loop_bound_lam4inv.py`**: Self-reproduced Lam4Inv comparison path. We did not directly plug the original Lam4Inv implementation into LIFT because Lam4Inv is designed for its own SMT-format benchmarks, while LIFT benchmarks are C/Boogie programs that require LIFT-specific preprocessing before verification. This file therefore implements a LIFT-compatible invariant-inference and checking flow based on Lam4Inv.
- **`Check_loop_bound_lemur.py`**: Lemur comparison path. It translates LIFT loop-bound candidates into C/YAML inputs expected by Lemur, runs the external Lemur validator, and records verified, falsified, unknown, timeout, or error outcomes.
- **`prompt_gen_llmselfchoice.py`**: Prompt construction and LLM-call wrapper for the unified self-choice strategy.
- **`spilit.py`**: Helper utilities for splitting invariant predicates during invariant-analysis routines.

## Experiments

### Main Experiment (RQ1 & RQ2)

The main experiment implementation is in **`Check_loop_bound_newiter.py`**, which uses:
- **Guess**: Gemini-2.5-flash/DeepSeek-V3.1 for loop bound generation
- **Check**: ICE-DT for invariant inference and verification

### Alternative Invariant Inference Tools

Two alternative invariant inference tools are provided:
- **`Check_loop_bound_lam4inv.py`**: Uses the self-reproduced Lam4Inv invariant-inference path described above
- **`Check_loop_bound_lemur.py`**: Uses Lemur instead of ICE-DT

### Unified Strategy Experiment (RQ3 Part 1)

Files ending with `_llmselfchoice` correspond to the **unified strategy** experiment described in the paper's RQ3 (first part). In this strategy, the LLM directly chooses between conjunctive and lexicographic loop bounds in a single query, rather than using the progressive approach.

## Prerequisites

### System Requirements

- Python 3.8+
- Mono runtime (for Boogie verifier)
- ANTLR4 runtime
- gcc/g++ and make

### Environment Setup

**Linux (Ubuntu 18.04+):**

1. Install the [Mono environment](https://www.mono-project.com/download/stable/#download-lin)

2. Install `python3`, `gcc/g++`, `make` and the necessary pip packages:
   ```bash
   apt install -y gcc g++ make python3 python3-pip
   pip install pandas scipy sklearn antlr4-python3-runtime xlsxwriter openai pyyaml
   ```

3. Build `Boogie` in `ice/popl16_artifact/Boogie/Source`:
   ```bash
   msbuild Boogie.sln
   ```

4. Build `C5.0` in `ice/popl16_artifact/C50`:
   ```bash
   make clean; make all
   ```
   Then, copy all generated `c5.0.*` files into `ice/popl16_artifact/Boogie/Binaries`

5. Download `z3 4.8.9` from [Github](https://github.com/Z3Prover/z3/releases/download/z3-4.8.9/z3-4.8.9-x64-ubuntu-16.04.zip)
   
   Unzip the file, copy `bin/z3` into `ice/popl16_artifact/Boogie/Binaries` and rename it to `z3.exe`

### Environment Variables

**You must set up the following API environment variables before running the experiments:**

```bash
# For DeepSeek-V3.1-Terminus (llm_type=0)
export DPSK_API_KEY="your-deepseek-api-key"
export DPSK_API_BASE="your-deepseek-api-base-url"

# For Gemini-2.5-flash (llm_type=1)
export GEMINI_API_KEY="your-gemini-api-key"
export GEMINI_API_BASE="your-gemini-api-base-url"
```

### Boogie Verifier

The Boogie verifier should be located at:
```
./ice/popl16_artifact/Boogie/Binaries/Boogie.exe
```

## Configuration

Edit `config.yaml` to customize the verification settings:

### LLM Configuration

```yaml
llm_lb:
  type: 1  # LLM for loop bound generation
           # 0: DeepSeek-V3.1-Terminus
           # 1: Gemini-2.5-flash

llm_invariant:
  type: 1  # LLM for invariant generation (used by LLM-based invariant tools)
           # 0: DeepSeek-V3.1-Terminus
           # 1: Gemini-2.5-flash
```

### Directory Configuration

```yaml
directories:
  tmp_dir: "/tmpfs/tmp"                                      # Temporary working directory
  input_dir: "/root/LIFT/experiment/benchmarks-Instrumented" # Input Boogie files (conjunctive benchmarks)
  input_lex_dir: "/root/LIFT/experiment/benchmarks-Instrumented-Lexicographic"  # Lexicographic benchmarks
```

### Verification Parameters

```yaml
verification:
  max_conj_iterations: 5       # Max iterations for conjunctive phase
  max_lex_iterations: 15       # Max iterations for lexicographic phase
  k_induction_max: 3           # Maximum K value for K-induction
  timeout_per_verification: 60 # Timeout per verification (seconds)
```

### Logging and Output Configuration

```yaml
logging:
  log_dir: "logs/"
  log_filename: "LIFT.log"

output:
  result_filename: "results/LIFT.txt"
```

### File List

```yaml
# File List to Process
# If empty, all files in input_dir will be processed
file_list:
- example_file_1
- example_file_2
```

## Usage

All verification scripts require the `-c` parameter to specify the configuration file:

```bash
cd /root/LIFT/
# Main experiment (Gemini/DeepSeek for guess + ICE-DT for check)
python ./code/Guess_Check/Check_loop_bound_newiter.py -c ./code/Guess_Check/config.yaml

# Alternative with Lam4Inv for invariant inference
python ./code/Guess_Check/Check_loop_bound_lam4inv.py -c ./code/Guess_Check/config.yaml

# Alternative with Lemur for invariant inference
python ./code/Guess_Check/Check_loop_bound_lemur.py -c ./code/Guess_Check/config.yaml

# Unified strategy experiment (RQ3 Part 1)
python ./code/Guess_Check/Check_loop_bound_llmselfchoice.py -c ./code/Guess_Check/config.yaml
```

**Configuration Steps:**

1. Edit `config.yaml` to specify:
   - `llm_lb.type`: LLM for loop bound generation (0=DeepSeek, 1=Gemini)
   - `llm_invariant.type`: LLM for invariant generation (0=DeepSeek, 1=Gemini)
   - `directories.input_dir`: Path to input Boogie benchmark files
   - `file_list`: List of specific files to process (leave empty to process all files in `input_dir`)
   
2. Run the desired experiment script with the `-c config.yaml` parameter

## Verification Workflow

The LIFT framework follows this workflow:

1. **Input Parsing**: Read Boogie program and extract loop structure
2. **Conjunctive Phase**: 
   - Generate conjunctive loop bounds via LLM
   - Apply K-transformation for verification
   - If verification fails, provide diagnostic feedback
   - Repeat up to `max_conj_iterations` times
3. **Lexicographic Phase** (if conjunctive fails):
   - Generate lexicographic (multi-component) loop bounds
   - Verify with extended K-transformation
   - Repeat up to `max_lex_iterations` times
4. **Output**: Log results and success/failure status

## Loop Bound Format

### Conjunctive Bounds

Single expression bounding the loop counter:
```
assume(i >= n);  // Loop terminates when i reaches n
```

### Lexicographic Bounds

Multiple components for nested or complex loops:
```
assume(i0 >= x && i1 >= y);  // Two-component lexicographic bound
```

## Diagnostic Feedback Types

When verification fails, LIFT provides feedback to guide the LLM:

| Type | Description |
|------|-------------|
| 1 | Grammar/syntax error |
| 2 | Verification failed (bound too small) |
| 3 | Verification timeout |

## Output Files

- **Log file**: Detailed verification log with timestamps, loop bounds tried, and results
- **Result file**: Summary of verification outcomes for all processed files


## Experiment Results

All experiment results and baseline comparison data are stored in the `../result_logs/` directory. See `../result_logs/README.md` for detailed information about:
- Result files for progressive and unified generation strategies
- Baseline tool results (ddlTerm, Proton, UAutomizer, Freqhorn, etc.)
- Analysis scripts for processing and comparing results

## Reference

This implementation is the artifact for the paper:

> **LIFT: LLM-Guided Loop Bound Generation for Program Termination Verification**
> The paper presents a framework that leverages LLMs to generate loop bounds as termination arguments, 
> using a guess-and-check methodology with diagnostic feedback for iterative refinement.
