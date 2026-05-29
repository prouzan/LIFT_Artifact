#!/usr/bin/env python3
"""
Analyze loop_bound_lemur_verification_gemini.log to compute:
1) Per-file per-iteration stats: infer_time, verification_time, tokens.
2) Total Inference Time (sum of infer_time across all entries).
3) Total Verification Time (sum of verification_time across all entries).
4) Average Time on Solved files: for each file, sum infer+verification from
   its first entry up to (and including) the first succeeded entry, then
   average across succeeded files.
"""

import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
LOG_PATH = ROOT / "loop_bound_lemur_verification_gemini.log"

# Patterns
PAT_FILE = re.compile(r"file:\s*([^\s,]+)")
PAT_FEEDBACK = re.compile(r"feed_back_iter:\s*([0-9]+)")
PAT_INFER = re.compile(r"infer_time:\s*([0-9.+eE-]+)")
PAT_VERIFY = re.compile(r"verification_time:\s*([0-9.+eE-]+)")
PAT_TOKENS = re.compile(r"tokens:\s*([0-9]+)")


def parse_log():
    records = []
    current_file = None
    current_file_c = None
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            lower = line.lower()
            # Track current processing file for fallback when success lines omit file field
            if "processing:" in lower:
                # Example: "Processing: FooBar"
                parts = line.strip().split("Processing:", 1)
                if len(parts) == 2:
                    current_file = parts[1].strip()
                    current_file_c = None
            if ".c" in line and "Processing:" in line:
                current_file_c = None

            # Skip const-add lines (repeats)
            if "const-add" in lower:
                continue

            if "verification " not in lower:
                continue

            result = None
            if "verification succeeded" in lower:
                result = "succeeded"
            elif "verification failed" in lower:
                result = "failed"
            elif "verification timed out" in lower:
                result = "timed_out"
            elif "verification unknown" in lower:
                result = "unknown"
            else:
                continue

            m_file = PAT_FILE.search(line)
            m_fb = PAT_FEEDBACK.search(line)
            m_infer = PAT_INFER.search(line)
            m_ver = PAT_VERIFY.search(line)
            m_tok = PAT_TOKENS.search(line)

            file_name = m_file.group(1) if m_file else None
            if file_name is None and current_file:
                # Try to append .c if missing; keep original
                file_name = current_file if current_file.endswith(".c") else f"{current_file}.c"

            rec = {
                "line": line.strip(),
                "file": file_name,
                "feed_back_iter": int(m_fb.group(1)) if m_fb else None,
                "infer_time": float(m_infer.group(1)) if m_infer else 0.0,
                "verification_time": float(m_ver.group(1)) if m_ver else 0.0,
                "tokens": int(m_tok.group(1)) if m_tok else None,
                "result": result,
            }
            if rec["file"] is not None:
                records.append(rec)
    return records


def main():
    records = parse_log()
    PRINT_DETAILS = False

    # Per-file per-iter stats
    per_file_iters = defaultdict(list)
    for r in records:
        per_file_iters[r["file"]].append(r)

    # Totals
    total_infer = sum(r["infer_time"] for r in records)
    total_ver = sum(r["verification_time"] for r in records)

    # Average time on solved files
    solved_times = []
    for fname, recs in per_file_iters.items():
        recs_sorted = sorted(recs, key=lambda x: x["feed_back_iter"] if x["feed_back_iter"] is not None else 1e9)
        acc = 0.0
        success_found = False
        for r in recs_sorted:
            acc += r["infer_time"] + r["verification_time"]
            if r["result"] == "succeeded":
                success_found = True
                break
        if success_found:
            solved_times.append(acc)

    avg_time_on_solved = sum(solved_times) / len(solved_times) if solved_times else 0.0

    # Output
    print("Total entries:", len(records))
    print(f"Total Inference Time: {total_infer:.3f}s")
    print(f"Total Verification Time: {total_ver:.3f}s")
    print(f"Solved files count: {len(solved_times)}")
    print(f"Average Time On Solved files: {avg_time_on_solved:.3f}s")
    print("\nPer-file per-iteration (file, iter, infer_time, verification_time, tokens, result):")
    if PRINT_DETAILS:
        for fname, recs in per_file_iters.items():
            for r in sorted(recs, key=lambda x: x.get('feed_back_iter', 0)):
                print(f"{fname}\titer={r['feed_back_iter']}\tinfer={r['infer_time']:.3f}\tverify={r['verification_time']:.3f}\ttokens={r['tokens']}\tresult={r['result']}")
    else:
        print("[Details suppressed; set PRINT_DETAILS=True to see all rows]")


if __name__ == "__main__":
    main()
