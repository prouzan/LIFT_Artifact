import json
import pickle
import re
from pathlib import Path
from typing import Callable, Dict, List, Tuple

import matplotlib.pyplot as plt

ROOT = Path(__file__).parent.parent
PROTON_LOG = ROOT / "proton-batch.log"
UA_LOG = ROOT / "UAutomizer.log"
PICKLE_FILE = ROOT / "Result_bench-term_TO120_B_All.rst"
DDL_LOG = ROOT / "ddlterm_new.log"
OUT_TOTALS = ROOT / "analysis_results" / "duration_totals.png"
OUT_AVGS = ROOT / "analysis_results" / "duration_avgs.png"


def aggregate(entries: List[Dict], true_pred: Callable[[Dict], bool]) -> Dict[str, float]:
    total = sum(e["dur_adj"] for e in entries)
    avg = total / len(entries) if entries else 0.0
    true_entries = [e for e in entries if true_pred(e)]
    true_total = sum(e["dur_adj"] for e in true_entries)
    true_avg = true_total / len(true_entries) if true_entries else 0.0
    return {
        "count": len(entries),
        "total": total,
        "avg": avg,
        "true_count": len(true_entries),
        "true_total": true_total,
        "true_avg": true_avg,
    }


def load_proton() -> Dict:
    entries = []
    for line in PROTON_LOG.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        entry = json.loads(line)
        dur = float(entry["duration_seconds"])
        # subtract first 10s for TRUE results as non-terminating check phase
        dur_adj = dur if str(entry.get("result", "")).startswith("TRUE") else dur
        entries.append({"status": entry.get("result"), "dur": dur, "dur_adj": dur_adj})
    return aggregate(entries, lambda e: str(e["status"]).startswith("TRUE"))


def load_uautomizer() -> Dict:
    lines = [ln.strip() for ln in UA_LOG.read_text().splitlines() if ln.strip()]
    if lines and lines[0].startswith("nohup:"):
        lines = lines[1:]
    entries = []
    i = 0
    while i + 1 < len(lines):
        # name line is lines[i]
        res = lines[i + 1]
        i += 2
        parts = res.split()
        status = None
        dur = None
        if len(parts) >= 2 and re.match(r"[-+]?\d", parts[1]):
            status = parts[0]
            dur = float(parts[1])
        elif len(parts) == 1:
            tok = parts[0]
            if re.fullmatch(r"[-+]?\d*\.?\d+", tok):
                status = "UNKNOWN"
                dur = float(tok)
            else:
                status = tok
                dur = float("nan")
        else:
            continue
        entries.append({"status": status, "dur": dur, "dur_adj": dur})
    return aggregate(entries, lambda e: str(e["status"]).upper().startswith("TRUE"))


def load_freqhorn() -> Dict:
    data = pickle.load(open(PICKLE_FILE, "rb"))["freqhornR3"]
    entries = [
        {"status": status, "dur": float(dur), "dur_adj": float(dur)}
        for status, dur in data.values()
    ]
    return aggregate(entries, lambda e: str(e["status"]).lower().startswith("termination"))

def load_freq_spacer() -> Dict:
    data = pickle.load(open(PICKLE_FILE, "rb"))["spacerR3"]
    entries = [
        {"status": status, "dur": float(dur), "dur_adj": float(dur)}
        for status, dur in data.values()
    ]
    return aggregate(entries, lambda e: str(e["status"]).lower().startswith("termination"))

def load_ddlterm() -> Dict:
    text = DDL_LOG.read_text()
    entries = []
    for match in re.finditer(
        r"Result:\s*(Termination|Failed)\s*\(([-+]?\d*\.?\d+)\s*s\)", text
    ):
        status = match.group(1)
        dur = float(match.group(2))
        entries.append({"status": status, "dur": dur, "dur_adj": dur})
    return aggregate(entries, lambda e: e["status"] == "Termination")


def plot_bars(
    stats: Dict[str, Dict[str, float]],
    metrics: List[Tuple[str, str]],
    title: str,
    outfile: Path,
):
    tools = list(stats.keys())
    hatch_patterns = ["///", "\\\\", "...", "xxx", "***"]

    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(metrics))
    width = 0.18

    for idx, tool in enumerate(tools):
        vals = [stats[tool][key] for _, key in metrics]
        bars = ax.bar(
            [p + (idx - (len(tools) - 1) / 2) * width for p in x],
            vals,
            width,
            label=tool,
            hatch=hatch_patterns[idx % len(hatch_patterns)],
            edgecolor="black",
            alpha=0.9,
        )
        ax.bar_label(bars, fmt="%.1f", fontsize=8)

    ax.set_xticks(list(x))
    ax.set_xticklabels([m[0] for m in metrics], fontsize=10)
    ax.set_ylabel("Seconds", fontsize=11)
    ax.set_title(title, fontsize=12)
    ax.legend(title="Tool", fontsize=9)
    ax.grid(True, axis="y", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(outfile, dpi=300)
    print(f"Saved figure to {outfile}")


def main():
    proton_stats = load_proton()
    uauto_stats = load_uautomizer()
    freq_stats = load_freqhorn()
    freq_spacer_stats = load_freq_spacer()
    ddl_stats = load_ddlterm()

    stats = {
        "Proton": proton_stats,
        "UAutomizer": uauto_stats,
        "Freqhorn": freq_stats,
        "FreqSpacer": freq_spacer_stats,
        "ddlTerm": ddl_stats,
    }

    print("Runtime statistics (seconds):")
    for tool, st in stats.items():
        print(
            f"- {tool}: total={st['total']:.3f}, avg={st['avg']:.3f}, "
            f"TRUE total={st['true_total']:.3f}, TRUE avg={st['true_avg']:.3f}, "
            f"count={st['count']}, TRUE count={st['true_count']}"
        )

    metrics_totals = [("Total (s)", "total"), ("TRUE Total (s)", "true_total")]
    metrics_avgs = [("Avg (s)", "avg"), ("TRUE Avg (s)", "true_avg")]

    plot_bars(
        stats,
        metrics_totals,
        "Runtime Totals (Proton TRUE subtracts first 10s)",
        OUT_TOTALS,
    )
    plot_bars(
        stats,
        metrics_avgs,
        "Runtime Averages (Proton TRUE subtracts first 10s)",
        OUT_AVGS,
    )


if __name__ == "__main__":
    main()
