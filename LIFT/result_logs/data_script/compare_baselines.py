#!/usr/bin/env python3
"""
Compare LIFT_default successes with baselines.
- Extract total files from LIFT_default log, succeeded list, and not-succeeded list.
- Compare LIFT_default vs LIFT_DeekSeek and all other baselines.
- Match by filename stem (remove only the last extension).
"""

import json
import pickle
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
LIFT_DEFAULT = ROOT / "LIFT_Gemini.log"
LIFT_DEEKSEEK = ROOT / "LIFT_DeekSeek.log"
DDLTERM = ROOT / "ddlterm_new.log"
PROTON = ROOT / "proton-batch.log"
LOOPY_DPSK = ROOT / "loopy_dpsk.json"
LOOPY_GEMINI = ROOT / "loopy_gemini_new.json"
UAUTOMIZER = ROOT / "UAutomizer.log"
FREQ_RST = ROOT / "Result_bench-term_TO120_B_All.rst"

OUTPUT_FILE = ROOT / "analysis_results" / "baseline_comparison_results.txt"

FILE_RE = re.compile(r"file:\s*([^,\s]+)")
KNOWN_EXTS = {".c", ".bpl", ".smt2", ".json"}


def base_name(path_or_name: str) -> str:
    name = Path(str(path_or_name).strip()).name
    name = name.strip().strip(",")
    suffix = Path(name).suffix
    if suffix in KNOWN_EXTS:
        return Path(name).stem
    return name


def parse_lift_log(path: Path):
    all_files = set()
    succeeded = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        m = FILE_RE.search(line)
        if not m:
            continue
        fname = base_name(m.group(1))
        all_files.add(fname)
        if "verification succeeded" in line.lower():
            succeeded.add(fname)
    return all_files, succeeded


def parse_ddlterm(path: Path):
    success = set()
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("[Info] Task "):
            current = line.split("[Info] Task ", 1)[1].strip()
        if line.startswith("[Info] Result:") and current:
            if "Termination" in line:
                success.add(base_name(current))
    return success


def parse_proton(path: Path):
    success = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        result = str(entry.get("result", ""))
        if result.startswith("TRUE"):
            success.add(base_name(entry.get("file", "")))
    return success


def parse_uautomizer(path: Path):
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if lines and lines[0].startswith("nohup:"):
        lines = lines[1:]
    success = set()
    i = 0
    while i + 1 < len(lines):
        name = lines[i]
        res = lines[i + 1]
        i += 2
        parts = res.split()
        status = parts[0] if parts else ""
        if status.upper().startswith("TRUE"):
            success.add(base_name(name))
    return success


def read_json_allow_null(path: Path):
    data = path.read_bytes().replace(b"\x00", b"")
    return json.loads(data.decode("utf-8", errors="ignore"))


def parse_loopy_json(path: Path):
    data = read_json_allow_null(path)
    stats = data.get("stats", {})
    success_list = stats.get("success", []) or []
    return {base_name(item) for item in success_list}


def parse_freq_rst(path: Path):
    data = pickle.load(open(path, "rb"))
    results = {}
    for key, entries in data.items():
        success = set()
        for fname, (status, _dur) in entries.items():
            if str(status).lower().startswith("termination"):
                success.add(base_name(fname))
        results[key] = success
    return results


def format_list(items):
    return "\n".join(f"- {name}" for name in sorted(items))


def main():
    lift_all, lift_success = parse_lift_log(LIFT_DEFAULT)
    lift_failed = lift_all - lift_success

    lift_default_summary = [
        f"LIFT_default total files: {len(lift_all)}",
        f"LIFT_default succeeded: {len(lift_success)}",
        f"LIFT_default not succeeded: {len(lift_failed)}",
    ]

    _, deekseek_success = parse_lift_log(LIFT_DEEKSEEK)
    default_only = lift_success - deekseek_success
    deekseek_only = deekseek_success - lift_success

    baseline_sets = {
        "ddlterm_new": parse_ddlterm(DDLTERM),
        "proton-batch": parse_proton(PROTON),
        "loopy_dpsk": parse_loopy_json(LOOPY_DPSK),
        "loopy_gemini_new": parse_loopy_json(LOOPY_GEMINI),
        "UAutomizer": parse_uautomizer(UAUTOMIZER),
    }

    freq_sets = parse_freq_rst(FREQ_RST)
    baseline_sets.update({"freqhornR3": freq_sets.get("freqhornR3", set())})
    baseline_sets.update({"spacerR3": freq_sets.get("spacerR3", set())})

    lines = []
    lines.append("=== LIFT_default summary ===")
    lines.extend(lift_default_summary)
    lines.append("\nLIFT_default succeeded list:")
    lines.append(format_list(lift_success))
    lines.append("\nLIFT_default not succeeded list:")
    lines.append(format_list(lift_failed))

    lines.append("\n=== LIFT_default vs LIFT_DeekSeek ===")
    lines.append(f"Default-only successes: {len(default_only)}")
    lines.append(format_list(default_only))
    lines.append("\nDeekSeek-only successes: {0}".format(len(deekseek_only)))
    lines.append(format_list(deekseek_only))

    lines.append("\n=== LIFT_default vs baselines ===")
    for name, success_set in baseline_sets.items():
        main_only = lift_success - success_set
        base_only = success_set - lift_success
        lines.append(f"\n[{name}]")
        lines.append(f"Main-only: {len(main_only)}")
        lines.append(format_list(main_only))
        lines.append(f"Baseline-only: {len(base_only)}")
        lines.append(format_list(base_only))

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")

    print("Summary:")
    print("\n".join(lift_default_summary))
    print(f"LIFT_default vs LIFT_DeekSeek: default-only={len(default_only)}, deekseek-only={len(deekseek_only)}")
    print("Baseline comparisons written to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
