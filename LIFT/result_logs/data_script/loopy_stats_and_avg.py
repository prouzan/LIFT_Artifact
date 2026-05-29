#!/usr/bin/env python3
"""
Fix stats in JSON result files and compute average time on solved.

Rules:
- success_count = len(stats["success"])
- failure_count = len(stats["failure"])
- Remove "total" and "success_rate" from stats if present.
- Average Time on Solved = sum(total_time_seconds for logs with success==True) / #successes

Outputs per file and a combined summary.
"""

import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
FILES = [
    ROOT / "loopy_dpsk.json",
    ROOT / "loopy_gemini_new.json",
]


def process_file(path: Path):
    data = json.loads(path.read_text(encoding="utf-8"))
    stats = data.get("stats", {})

    success_list = stats.get("success", []) or []
    failure_list = stats.get("failure", []) or []
    stats["success_count"] = len(success_list)
    stats["failure_count"] = len(failure_list)
    # Drop fields
    stats.pop("total", None)
    stats.pop("success_rate", None)
    data["stats"] = stats

    # Average time on solved
    logs = data.get("logs", [])
    solved_times = [entry.get("total_time_seconds", 0.0) for entry in logs if entry.get("success")]
    avg_time = sum(solved_times) / len(solved_times) if solved_times else 0.0

    # Persist changes
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "file": str(path),
        "success_count": stats["success_count"],
        "failure_count": stats["failure_count"],
        "avg_time_on_solved": avg_time,
        "solved_files": len(solved_times),
    }


def main():
    results = [process_file(p) for p in FILES]
    combined_solved = sum(r["solved_files"] for r in results)
    combined_time = 0.0
    # Recompute combined time by re-reading to avoid double compute
    for p in FILES:
        data = json.loads(p.read_text(encoding="utf-8"))
        logs = data.get("logs", [])
        for entry in logs:
            if entry.get("success"):
                combined_time += entry.get("total_time_seconds", 0.0)

    combined_avg = combined_time / combined_solved if combined_solved else 0.0

    print("Per-file stats:")
    for r in results:
        print(
            f"- {r['file']}: success_count={r['success_count']}, "
            f"failure_count={r['failure_count']}, "
            f"avg_time_on_solved={r['avg_time_on_solved']:.3f}s "
            f"(solved_files={r['solved_files']})"
        )
    print("\nCombined:")
    print(f"- solved_files={combined_solved}")
    print(f"- avg_time_on_solved={combined_avg:.3f}s")


if __name__ == "__main__":
    main()
