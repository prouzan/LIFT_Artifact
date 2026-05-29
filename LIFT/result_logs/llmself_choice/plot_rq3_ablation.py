import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def extract_succeeded_count(log_file_path: Path) -> int:
    """Extract the count of unique files with successful verification from a log file."""
    succeeded_files = set()
    pattern = re.compile(r'Verification succeeded.*?file: ([^,]+)')
    
    with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                succeeded_files.add(match.group(1))
    
    return len(succeeded_files)


def main() -> None:
    # Data extracted from log files
    configs = [
        "DeepSeek\nNoThinking",
        "DeepSeek\nThinking",
        "Gemini\nNoThinking",
        "Gemini\nThinking",
    ]

    # Define log file paths
    logs_dir = Path(__file__).resolve().parent.parent
    llmself_choice_dir = logs_dir / "llmself_choice"
    lift_dir = logs_dir / "LIFT"

    # Progressive vs Unified (Guidance = Yes)
    # Progressive: LIFT folder files without nodiagn suffix
    progressive_guidance_yes = [
        extract_succeeded_count(lift_dir / "LIFT_DeekSeek_nothinking.log"),
        extract_succeeded_count(lift_dir / "LIFT_DeekSeek_thinking.log"),
        extract_succeeded_count(lift_dir / "LIFT_Gemini_nothinking.log"),
        extract_succeeded_count(lift_dir / "LIFT_Gemini_thinking.log"),
    ]

    # Unified: llmself_choice folder files
    unified_guidance_yes = [
        extract_succeeded_count(llmself_choice_dir / "dpsk_v31_nothinking_llmselfchoice.log"),
        extract_succeeded_count(llmself_choice_dir / "dpsk_v31_thinking_llmselfchoice.log"),
        extract_succeeded_count(llmself_choice_dir / "gemini_nothinking_llmselfchoice.log"),
        extract_succeeded_count(llmself_choice_dir / "gemini_thinking_llmselfchoice.log"),
    ]

    # Guidance ablation under Progressive generation
    # Progressive without diagnostic messages: LIFT folder files with nodiagn suffix
    progressive_guidance_no = [
        extract_succeeded_count(lift_dir / "LIFT_DeepSeek_nothinking_nodiagn.log"),
        extract_succeeded_count(lift_dir / "LIFT_DeepSeek_thinking_nodiagn.log"),
        extract_succeeded_count(lift_dir / "LIFT_Gemini_nothinking_nodiagn.log"),
        extract_succeeded_count(lift_dir / "LIFT_Gemini_thinking_nodiagn.log"),
    ]

    x = np.arange(len(configs))
    w = 0.36

    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.size": 9,
            "axes.labelsize": 9,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
        }
    )

    # Muted palette consistent with paper (blue + purple) and accessible via hatches.
    teal_raw = "#008080"
    gray_raw = "#6B6B6B"
    blue = "#C3E2EC"
    purple = "#E3C6E0"
    

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 2.55), constrained_layout=False)
    fig.subplots_adjust(left=0.07, right=0.995, top=0.83, bottom=0.30, wspace=0.25)

    # (a) Progressive vs Unified
    ax = axes[0]
    b1 = ax.bar(
        x - w / 2,
        progressive_guidance_yes,
        width=w,
        label="Progressive",
        color=blue,
        edgecolor="black",
        linewidth=0.6,
        hatch="//",
    )
    b2 = ax.bar(
        x + w / 2,
        unified_guidance_yes,
        width=w,
        label="Unified",
        color=purple,
        edgecolor="black",
        linewidth=0.6,
        hatch="\\\\",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(configs)
    ax.set_ylabel("Verified Benchmarks")
    ax.grid(axis="y", linestyle=":", linewidth=0.6)
    ax.text(
        0.5,
        -0.30,
        "(a) Progressive vs Unified (Diagnostic Message)",
        transform=ax.transAxes,
        ha="center",
        va="top",
    )

    # (b) Guidance ablation
    ax = axes[1]
    b3 = ax.bar(
        x - w / 2,
        progressive_guidance_no,
        width=w,
        label="Feedback without Diagnostic Message",
        color=blue,
        edgecolor="black",
        linewidth=0.6,
        hatch="..",
    )
    b4 = ax.bar(
        x + w / 2,
        progressive_guidance_yes,
        width=w,
        label="Feedback with Diagnostic Message",
        color=purple,
        edgecolor="black",
        linewidth=0.6,
        hatch="xx",
    )
    ax.set_xticks(x)
    ax.set_xticklabels(configs)
    ax.grid(axis="y", linestyle=":", linewidth=0.6)
    ax.text(
        0.5,
        -0.30,
        "(b) Diagnostic Message Ablation (Progressive generation)",
        transform=ax.transAxes,
        ha="center",
        va="top",
    )

    # Annotate bars with values
    for bars in (b1, b2, b3, b4):
        for rect in bars:
            h = rect.get_height()
            ax_ = rect.axes
            ax_.text(
                rect.get_x() + rect.get_width() / 2,
                h + 1.2,
                f"{int(h)}",
                ha="center",
                va="bottom",
                fontsize=7,
            )

    # Shared y-limits for comparability
    y_max = max(
        max(progressive_guidance_yes),
        max(unified_guidance_yes),
        max(progressive_guidance_no),
    )
    y_min = 130
    y_top = 170
    for ax in axes:
        ax.set_ylim(y_min, y_top)
        ax.set_yticks(np.arange(y_min, y_top + 1, 5))

    handles, labels = axes[0].get_legend_handles_labels()
    handles2, labels2 = axes[1].get_legend_handles_labels()
    # Keep a single shared legend above subplots.
    fig.legend(
        handles + handles2,
        labels + labels2,
        loc="upper center",
        ncol=4,
        frameon=True,
        bbox_to_anchor=(0.5, 0.995),
        columnspacing=1.2,
        handlelength=1.8,
    )

    out_dir = Path(r"./output_figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    pdf_path = out_dir / "rq3_ablation.pdf"
    png_path = out_dir / "rq3_ablation.png"

    fig.savefig(pdf_path, bbox_inches="tight")
    fig.savefig(png_path, dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
