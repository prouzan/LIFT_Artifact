# Experiment Results

This directory contains all experiment results for the LIFT framework and baseline tool comparisons.

## Result File Organization

### LIFT Results

#### Progressive Generation Strategy (Main Experiments)

Located in the `LIFT/` subdirectory:
- **`LIFT_Gemini.log`**: LIFT results using Gemini-2.5-flash for loop bound generation with ICE-DT for verification
- **`LIFT_DeepSeek.log`**: LIFT results using DeepSeek-V3.1-Terminus for loop bound generation with ICE-DT for verification

These files contain detailed logs of the verification process with progressive generation strategy (conjunctive → lexicographic).

#### Unified Generation Strategy (RQ3 Part 1)

Located in the `llmself_choice/` subdirectory:
- Results for the unified strategy experiment where the LLM directly chooses between conjunctive and lexicographic bounds in a single query

### Baseline Tool Results

The following baseline tool results are provided for comparison:

- **`ddlterm_new.log`**: ddlTerm verification results
- **`proton-batch.log`**: Proton verification results (JSON format)
- **`UAutomizer.log`**: UAutomizer verification results
- **`loopy_dpsk.json`**: Loopy tool results using DeepSeek
- **`loopy_gemini_new.json`**: Loopy tool results using Gemini
- **`Result_bench-term_TO120_B_All.rst`**: Freqterm results (pickled format)

## Analysis Scripts

We provide analysis scripts in the `data_script/` subdirectory to process and compare the experiment results:

### 1. `analyze_LIFT_log.py`

Analyzes LIFT log files to extract detailed verification statistics.

**Usage:**
```bash
cd data_script
python analyze_LIFT_log.py --log ../LIFT/LIFT_Gemini.log
```

**Outputs:**
- Number of solved test cases
- Total verification time
- Average verification time per benchmark
- Feedback iteration statistics
- Token usage statistics
- Success rate by bound type (conjunctive vs lexicographic)

### 2. `compare_baselines.py`

Compares LIFT results with baseline tools to identify uniquely solved benchmarks.

**Usage:**
```bash
cd data_script
python compare_baselines.py
```

**Outputs:**
- LIFT-only successes (benchmarks solved only by LIFT)
- Baseline-only successes (benchmarks solved only by each baseline)
- Comparison between LIFT_Gemini and LIFT_DeepSeek
- Detailed file lists for each comparison

**Output File:** `analysis_results/baseline_comparison_results.txt`

### 3. `duration_stats.py`

Compares runtime statistics across all baseline tools.

**Usage:**
```bash
cd data_script
python duration_stats.py
```

**Outputs:**
- Average runtime per benchmark (all and successful cases)
- Statistical comparison across tools
- Visualization plots (PNG format)

**Output Files:**
- `analysis_results/duration_avgs.png`: Runtime averages comparison chart
- `analysis_results/duration_totals.png`: Runtime totals comparison chart

### 4. `loopy_stats_and_avg.py`

Processes Loopy JSON result files to fix statistics and compute average time on solved benchmarks.

**Usage:**
```bash
cd data_script
python loopy_stats_and_avg.py
```

**Operations:**
- Fixes `success_count` and `failure_count` in stats
- Removes `total` and `success_rate` fields from stats
- Computes average time on solved benchmarks
- Updates JSON files in place

**Outputs:**
- Per-file statistics (success/failure counts, average time)
- Combined statistics across both Loopy result files

### 5. `analyze_loop_bound_lemur.py`

Analyzes LEMUR verification logs to compute detailed statistics.

**Usage:**
```bash
cd data_script
python analyze_loop_bound_lemur.py
```

**Outputs:**
- Total inference time
- Total verification time
- Solved files count
- Average time on solved files
- Per-file per-iteration statistics (optional, set `PRINT_DETAILS=True`)

## Notes

- All log files use UTF-8 encoding
- JSON files may contain null bytes and are handled appropriately by the analysis scripts
- The pickled `.rst` file contains results for Freqterm experiments
- LIFT log files include detailed information about each verification attempt, including:
  - Loop bounds generated
  - Verification results
  - Counterexamples (when applicable)
  - Inference and verification times
  - Token usage

## File Format Details

### LIFT Log Format

Each log entry contains:
```
YYYY-MM-DD HH:MM:SS - INFO: Verification [succeeded/failed/timeout] with the loop bound: [bound], 
file: [filename], k: [k-value], verification_time: [time], infer_time: [time], 
feed_back_iter: [iteration], tokens: [count]
```

### Baseline Log Formats

- **ddlterm_new.log**: Text format with "Result: Termination/Failed (X.XX s)" entries
- **proton-batch.log**: JSONL format with `file`, `result`, `duration_seconds` fields
- **UAutomizer.log**: Text format with filename followed by result and time
- **loopy_*.json**: JSON format with `stats.success` array
- **Result_bench-term_TO120_B_All.rst**: Python pickle with nested dictionaries

## Reproducing Results

To reproduce the experiment results:

1. Configure the environment as described in `../code/Guess_Check/README.md`
2. Set up API keys for LLM access
3. Run the verification scripts with appropriate config files:
   ```bash
   cd ~/LIFT
   python3 ./code/Guess_Check/Check_loop_bound_newiter.py -c ./code/Guess_Check/config.yaml
   ```
4. Analyze results using the provided scripts in the `data_script/` directory
