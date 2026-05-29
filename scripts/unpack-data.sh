#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASELINE_TAR="$ROOT_DIR/data/baseline.scripts.tar.gz"
TARGET="$ROOT_DIR/LIFT/experiment/baseline.scripts"

cd "$ROOT_DIR"

if [[ ! -f "$BASELINE_TAR" ]]; then
  echo "Baseline data archive is missing. If this was a lightweight clone, run:" >&2
  echo "  git lfs pull --include='data/*.tar.gz'" >&2
  exit 1
fi

if [[ "$(wc -c < "$BASELINE_TAR")" -lt 1000000 ]]; then
  echo "Baseline data archive looks like a Git LFS pointer. Pull it with:" >&2
  echo "  git lfs pull --include='data/*.tar.gz'" >&2
  exit 1
fi

if [[ -e "$TARGET" && "${FORCE:-0}" != "1" ]]; then
  echo "$TARGET already exists. Set FORCE=1 to replace it." >&2
  exit 1
fi

echo "Checking baseline data archive..."
sha256sum -c data/SHA256SUMS

if [[ -e "$TARGET" ]]; then
  rm -rf "$TARGET"
fi

echo "Extracting baseline.scripts into LIFT/experiment/ ..."
tar -xzf "$BASELINE_TAR" -C "$ROOT_DIR/LIFT/experiment"

echo "Done."
