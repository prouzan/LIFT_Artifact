#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE_TAR="$ROOT_DIR/docker/lift-repro-ubuntu20.04-tools.tar.gz"

cd "$ROOT_DIR"

if [[ ! -f "$IMAGE_TAR" ]]; then
  echo "Docker image archive is missing. If this was a lightweight clone, run:" >&2
  echo "  git lfs pull --include='docker/*.tar.gz'" >&2
  exit 1
fi

if [[ "$(wc -c < "$IMAGE_TAR")" -lt 1000000 ]]; then
  echo "Docker image archive looks like a Git LFS pointer. Pull it with:" >&2
  echo "  git lfs pull --include='docker/*.tar.gz'" >&2
  exit 1
fi

echo "Checking Docker image archive..."
sha256sum -c docker/SHA256SUMS

echo "Loading Docker image lift-repro:ubuntu20.04-tools ..."
docker load -i "$IMAGE_TAR"

echo "Done. Try:"
echo "  docker run -it --rm -v \"$ROOT_DIR/LIFT:/root/LIFT\" -w /root/LIFT lift-repro:ubuntu20.04-tools"
