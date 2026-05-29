#!/usr/bin/env python3
"""
Statistics script for prev_ce_feedback log files.

Functions:
1. Find the unique succeeded line for each file, collect k and feed_back_iter, plot bar charts.
2. Collect max feed_back_iter per file and plot distribution.
3. Compute total infer_time (deduplicated by file+feed_back_iter) and verification_time, visualize iter vs time.
4. Count consecutive "has already been tried." blocks and report nearest file + loop bound.

Output:
- figures/succeeded_k.png
- figures/succeeded_feedback_iter.png
- figures/max_feedback_iter_per_file.png
- figures/iter_count_vs_time.png
- summary_prev_ce_feedback0.md
"""

import argparse
import os
import re
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt


LOG_LINE_PATTERNS = {
    "file": re.compile(r"file:\s*([^,\s]+\.bpl)"),
    "k": re.compile(r"k:\s*(-?\d+)"),
    "feed_back_iter": re.compile(r"feed_back_iter:\s*(-?\d+)"),
    "infer_time": re.compile(r"infer_time:\s*([0-9.+eE-]+)"),
    "loop_bound_infer_time": re.compile(r"loop_bound_infer_time:\s*([0-9.+eE-]+)"),
    "verification_time": re.compile(r"verification_time:\s*([0-9.+eE-]+)"),
    "tokens": re.compile(r"tokens:\s*([0-9]+)"),
}


def classify_result(line: str) -> Optional[str]:
    if "Verification succeeded" in line:
        return "succeeded"
    if "Verification failed" in line:
        return "failed"
    if "Verification timed out" in line:
        return "timed_out"
    if "Counter error" in line:
        return "counter_error"
    if "ICE Runtime error" in line:
        return "ice_runtime_error"
    return None


def parse_log(log_path: str):
    records = []
    blocks_already_tried = []

    last_filename = None
    in_block = False
    block_start = None
    block_bounds: List[str] = []
    block_prev_file = None
    block_lines: List[Tuple[int, str]] = []

    with open(log_path, "r", encoding="utf-8") as f:
        for line_num, raw in enumerate(f, 1):
            line = raw.strip()
            rec = {
                "line_num": line_num,
                "raw": line,
                "filename": None,
                "k": None,
                "feed_back_iter": None,
                "infer_time": None,
                "verification_time": None,
                "result": None,
                "has_already": False,
                "nearest_prev_file": last_filename,
                "tokens": None,
            }

            file_match = LOG_LINE_PATTERNS["file"].search(line)
            if file_match:
                rec["filename"] = file_match.group(1)
                last_filename = rec["filename"]
                rec["nearest_prev_file"] = last_filename

            for key in ("k", "feed_back_iter"):
                m = LOG_LINE_PATTERNS[key].search(line)
                if m:
                    rec[key] = int(m.group(1))

            m_loop_infer = LOG_LINE_PATTERNS["loop_bound_infer_time"].search(line)
            if m_loop_infer:
                rec["infer_time"] = float(m_loop_infer.group(1))
            else:
                m_infer = LOG_LINE_PATTERNS["infer_time"].search(line)
                if m_infer:
                    rec["infer_time"] = float(m_infer.group(1))

            m_veri = LOG_LINE_PATTERNS["verification_time"].search(line)
            if m_veri:
                rec["verification_time"] = float(m_veri.group(1))

            m_tokens = LOG_LINE_PATTERNS.get("tokens").search(line)
            if m_tokens:
                try:
                    rec["tokens"] = int(m_tokens.group(1))
                except Exception:
                    rec["tokens"] = None

            rec["result"] = classify_result(line)
            rec["has_already"] = "has already been tried" in line

            records.append(rec)

            if rec["has_already"]:
                if not in_block:
                    in_block = True
                    block_start = line_num
                    block_prev_file = last_filename
                    block_bounds = []
                    block_lines = []
                block_lines.append((line_num, line))
                bound_match = re.search(r"loop bound\s*([^\s].*?)\s*has already been tried", line)
                if bound_match:
                    block_bounds.append(bound_match.group(1))
            else:
                if in_block:
                    blocks_already_tried.append(
                        {
                            "start": block_start,
                            "end": line_num - 1,
                            "length": line_num - block_start,
                            "nearest_prev_file": block_prev_file,
                            "bounds": block_bounds,
                            "lines": block_lines,
                        }
                    )
                    in_block = False

    if in_block:
        blocks_already_tried.append(
            {
                "start": block_start,
                "end": records[-1]["line_num"],
                "length": records[-1]["line_num"] - block_start + 1,
                "nearest_prev_file": block_prev_file,
                "bounds": block_bounds,
                "lines": block_lines,
            }
        )

    return records, blocks_already_tried


def ensure_fig_dir(out_dir: str):
    os.makedirs(out_dir, exist_ok=True)


def plot_bar(data: Dict[str, float], title: str, xlabel: str, ylabel: str, out_path: str):
    if not data:
        return
    try:
        labels = sorted(data.keys(), key=lambda x: float(x))
    except Exception:
        labels = sorted(data.keys())
    values = [data[k] for k in labels]
    plt.figure(figsize=(max(6, len(labels) * 0.5), 5))
    bars = plt.bar(labels, values)
    for bar, val in zip(bars, values):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{val}",
            ha="center",
            va="bottom",
            fontsize=8,
            rotation=0,
        )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_scatter(avg_infer_by_iter: Dict[int, float], avg_ver_by_iter: Dict[int, float], out_path: str):
    """Plot average inference and verification time per iteration round."""
    if not avg_infer_by_iter and not avg_ver_by_iter:
        return
    
    all_iters = sorted(set(list(avg_infer_by_iter.keys()) + list(avg_ver_by_iter.keys())))
    y_infer = [avg_infer_by_iter.get(i, 0.0) for i in all_iters]
    y_ver = [avg_ver_by_iter.get(i, 0.0) for i in all_iters]

    plt.figure(figsize=(10, 6))
    plt.plot(all_iters, y_infer, alpha=0.7, label="avg_infer_time", marker="o", linestyle='-', linewidth=2)
    plt.plot(all_iters, y_ver, alpha=0.7, label="avg_verification_time", marker="x", linestyle='-', linewidth=2)
    plt.xlabel("feed_back_iter round")
    plt.ylabel("average time (seconds)")
    plt.title("Average Inference and Verification Time per Iter Round")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def plot_avg_infer_per_round(avg_infer_per_round: Dict[int, float], out_path: str):
    """Plot average inference time per feedback round."""
    if not avg_infer_per_round:
        return
    rounds = sorted(avg_infer_per_round.keys())
    avg_times = [avg_infer_per_round[r] for r in rounds]
    
    plt.figure(figsize=(10, 6))
    plt.plot(rounds, avg_times, marker='o', linestyle='-', linewidth=2, markersize=8)
    for r, t in zip(rounds, avg_times):
        plt.text(r, t, f"{t:.1f}", ha="center", va="bottom", fontsize=8)
    
    plt.xlabel("feed_back_iter round")
    plt.ylabel("average infer_time (seconds)")
    plt.title("Average Inference Time per Feedback Round")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


def analyze_one_log(log_path: str, output_base: str):
    log_stem = os.path.splitext(os.path.basename(log_path))[0]
    out_dir = os.path.join(output_base, log_stem)
    ensure_fig_dir(out_dir)
    summary_path = os.path.join(out_dir, f"summary_{log_stem}.md")

    records, blocks = parse_log(log_path)

    success_k = {}
    success_iter = {}
    for rec in records:
        if rec["result"] == "succeeded" and rec["filename"]:
            success_k[rec["filename"]] = rec["k"]
            success_iter[rec["filename"]] = rec["feed_back_iter"]

    k_dist = defaultdict(int)
    for val in success_k.values():
        k_dist[str(val)] += 1
    iter_dist = defaultdict(int)
    for val in success_iter.values():
        iter_dist[str(val)] += 1

    plot_bar(k_dist, "Succeeded files by k", "k value", "file count", os.path.join(out_dir, "succeeded_k.png"))
    plot_bar(iter_dist, "Succeeded files by feed_back_iter", "feed_back_iter", "file count", os.path.join(out_dir, "succeeded_feedback_iter.png"))

    max_iter = defaultdict(int)
    for rec in records:
        if rec["filename"] and rec["feed_back_iter"] is not None:
            if rec["feed_back_iter"] > max_iter[rec["filename"]]:
                max_iter[rec["filename"]] = rec["feed_back_iter"]
    max_iter_dist = defaultdict(int)
    for val in max_iter.values():
        max_iter_dist[str(val)] += 1
    plot_bar(max_iter_dist, "Files by max feed_back_iter", "max feed_back_iter", "file count", os.path.join(out_dir, "max_feedback_iter_per_file.png"))

    groups = defaultdict(list)
    for rec in records:
        if rec["filename"] and rec["feed_back_iter"] is not None:
            groups[(rec["filename"], rec["feed_back_iter"])].append(rec)

    infer_totals = defaultdict(float)
    iter_counts = defaultdict(int)
    for (fname, it), recs in groups.items():
        iter_counts[fname] += 1
        infer_val = next((r["infer_time"] for r in recs if r["infer_time"] is not None), None)
        if infer_val is not None:
            infer_totals[fname] += infer_val

    overall_infer_total = sum(infer_totals.values())

    ver_totals = defaultdict(float)
    overall_ver_total = 0.0
    has_loop_bound_infer = any(
        LOG_LINE_PATTERNS["loop_bound_infer_time"].search(r["raw"]) for r in records
    )
    for rec in records:
        if not rec["filename"]:
            continue
        vtime = rec["verification_time"]
        if vtime is None and rec["result"] == "timed_out" and not has_loop_bound_infer:
            vtime = 60.0
        if vtime is None:
            vtime = 0.0
        ver_totals[rec["filename"]] += vtime
        overall_ver_total += vtime

    infer_by_iter = defaultdict(list)
    ver_by_iter = defaultdict(list)
    
    for (fname, it), recs in groups.items():
        infer_val = next((r["infer_time"] for r in recs if r["infer_time"] is not None), None)
        if infer_val is not None:
            infer_by_iter[it].append(infer_val)
        
        ver_sum = 0.0
        for r in recs:
            vtime = r["verification_time"]
            if vtime is None and r["result"] == "timed_out" and not has_loop_bound_infer:
                vtime = 60.0
            if vtime is None:
                vtime = 0.0
            ver_sum += vtime
        if ver_sum > 0:
            ver_by_iter[it].append(ver_sum)
    
    avg_infer_by_iter = {}
    for it, times in infer_by_iter.items():
        avg_infer_by_iter[it] = sum(times) / len(times) if times else 0.0
    
    avg_ver_by_iter = {}
    for it, times in ver_by_iter.items():
        avg_ver_by_iter[it] = sum(times) / len(times) if times else 0.0
    
    plot_scatter(avg_infer_by_iter, avg_ver_by_iter, os.path.join(out_dir, "iter_count_vs_time.png"))

    succeeded_files = set(success_k.keys())
    succeeded_infer_times = [infer_totals[f] for f in succeeded_files if f in infer_totals]
    succeeded_ver_times = [ver_totals[f] for f in succeeded_files if f in ver_totals]
    
    avg_succeeded_infer = sum(succeeded_infer_times) / len(succeeded_infer_times) if succeeded_infer_times else 0.0
    avg_succeeded_ver = sum(succeeded_ver_times) / len(succeeded_ver_times) if succeeded_ver_times else 0.0

    round_infer_times = defaultdict(list)
    for (fname, it), recs in groups.items():
        infer_val = next((r["infer_time"] for r in recs if r["infer_time"] is not None), None)
        if infer_val is not None:
            round_infer_times[it].append(infer_val)
    
    avg_infer_per_round = {}
    for round_num, times in round_infer_times.items():
        avg_infer_per_round[round_num] = sum(times) / len(times) if times else 0.0
    
    plot_avg_infer_per_round(avg_infer_per_round, os.path.join(out_dir, "avg_infer_time_per_round.png"))

    token_by_iter = defaultdict(list)
    token_total_per_file = defaultdict(int)
    has_token = False
    for (fname, it), recs in groups.items():
        token_val = next((r["tokens"] for r in recs if r.get("tokens") is not None), None)
        if token_val is not None:
            has_token = True
            token_by_iter[it].append(token_val)
            token_total_per_file[fname] += token_val

    avg_token_by_iter = {}
    if has_token:
        for it, vals in token_by_iter.items():
            avg_token_by_iter[it] = sum(vals) / len(vals) if vals else 0.0
    overall_avg_total_tokens = (
        sum(token_total_per_file.values()) / len(token_total_per_file) if token_total_per_file else 0.0
    )

    already_block_count = len(blocks)

    with open(summary_path, "w", encoding="utf-8") as sf:
        sf.write(f"# {log_stem} Statistics\n\n")
        sf.write("## 1. Succeeded k and feed_back_iter\n")
        sf.write(f"- Succeeded file count: {len(success_k)}\n")
        sf.write(f"- Charts: {os.path.join(out_dir, 'succeeded_k.png')}, {os.path.join(out_dir, 'succeeded_feedback_iter.png')}\n\n")

        sf.write("## 2. Max feed_back_iter per file\n")
        sf.write(f"- File count: {len(max_iter)}\n")
        sf.write(f"- Chart: {os.path.join(out_dir, 'max_feedback_iter_per_file.png')}\n\n")

        sf.write("## 3. Time Statistics\n")
        sf.write(f"- Total infer_time (deduplicated by file+iter): {overall_infer_total:.3f}s\n")
        sf.write(f"- Total verification_time: {overall_ver_total:.3f}s\n")
        sf.write(f"- Iteration vs time scatter plot: {os.path.join(out_dir, 'iter_count_vs_time.png')}\n\n")
        
        sf.write("### 3.1 Average time for succeeded files\n")
        sf.write(f"- Succeeded file count: {len(succeeded_files)}\n")
        sf.write(f"- Average total infer_time (deduplicated by file+iter): {avg_succeeded_infer:.3f}s\n")
        sf.write(f"- Average total verification_time: {avg_succeeded_ver:.3f}s\n\n")
        
        sf.write("### 3.2 Average infer_time per round\n")
        sf.write(f"- Chart: {os.path.join(out_dir, 'avg_infer_time_per_round.png')}\n")
        if avg_infer_per_round:
            sf.write("- Details:\n")
            for round_num in sorted(avg_infer_per_round.keys()):
                sf.write(f"  - Round {round_num}: {avg_infer_per_round[round_num]:.3f}s\n")
        sf.write("\n")

        sf.write("## 4. Token Statistics (non-llmselfchoice logs)\n")
        if has_token:
            sf.write(f"- Files with token records: {len(token_total_per_file)}\n")
            sf.write(f"- Average total tokens across all files and iterations: {overall_avg_total_tokens:.1f}\n")
            if avg_token_by_iter:
                sf.write("- Average tokens per round:\n")
                for it in sorted(avg_token_by_iter.keys()):
                    sf.write(f"  - Round {it}: {avg_token_by_iter[it]:.1f}\n")
        else:
            sf.write("- No token field detected, token statistics skipped\n")
        sf.write("\n")

        sf.write("## 5. Consecutive \"has already been tried.\" blocks\n")
        sf.write(f"- Block count: {already_block_count}\n")
        if blocks:
            sf.write("### Details\n")
            for idx, b in enumerate(blocks, 1):
                sf.write(f"- Block {idx}: lines {b['start']} - {b['end']} (length {b['length']}), nearest file: {b['nearest_prev_file'] or 'unknown'}\n")
                if b["bounds"]:
                    sf.write(f"  - loop bounds: {', '.join(b['bounds'])}\n")
        sf.write("\n")

    print("Done. Please check the generated charts and files:")
    print(f"- {summary_path}")
    print(f"- {out_dir}/succeeded_k.png")
    print(f"- {out_dir}/succeeded_feedback_iter.png")
    print(f"- {out_dir}/max_feedback_iter_per_file.png")
    print(f"- {out_dir}/iter_count_vs_time.png")
    print(f"- {out_dir}/avg_infer_time_per_round.png")
    if has_token:
        print(f"- Token statistics written to summary")
    else:
        print(f"- No token field detected, token statistics skipped")


def main():
    parser = argparse.ArgumentParser(description="Analyze prev_ce logs (single or batch).")
    parser.add_argument("--log", help="single log file path")
    parser.add_argument("--log-dir", help="directory containing log files for batch mode")
    parser.add_argument(
        "--output-base",
        default=None,
        help="base directory to store generated files; default: analysis_outputs next to log or <log-dir>/analysis_outputs_batch",
    )
    args = parser.parse_args()

    logs_to_run: List[str] = []
    if args.log_dir:
        for fname in os.listdir(args.log_dir):
            if fname.lower().endswith(".log"):
                logs_to_run.append(os.path.join(args.log_dir, fname))
    if args.log:
        logs_to_run.append(args.log)

    if not logs_to_run:
        parser.error("Please provide --log or --log-dir with .log files.")

    if args.log_dir:
        output_base = args.output_base or os.path.join(args.log_dir, "analysis_outputs_batch")
    else:
        if args.output_base:
            output_base = args.output_base
        else:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_base = os.path.join(os.path.dirname(script_dir), "analysis_results")

    for lp in logs_to_run:
        analyze_one_log(lp, output_base)


if __name__ == "__main__":
    main()
