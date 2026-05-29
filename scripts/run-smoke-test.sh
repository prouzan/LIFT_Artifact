#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
IMAGE="${IMAGE:-lift-repro:ubuntu20.04-tools}"

docker run --rm \
  -v "$ROOT_DIR/LIFT:/root/LIFT" \
  -w /root/LIFT \
  "$IMAGE" \
  /bin/bash -lc 'python3 - <<'"'"'PY'"'"'
import os
import sys

sys.path.insert(0, "/root/LIFT/code/Guess_Check")
sys.path.insert(0, "/root/LIFT/code")

from Check_loop_bound_newiter import BoogieVerifier, extract_variables_from_bpl
from K_Transform import K_Transformer

origin = "/root/LIFT/experiment/benchmarks-Instrumented/for_bounded_loop1_false-unreach-call_true-termination-simplified/for_bounded_loop1_false-unreach-call_true-termination-simplified.bpl"
tmp = "/tmpfs/tmp/lift_smoke"
os.makedirs(tmp, exist_ok=True)

loop_bound = [("i", "n - _i")]
transformer = K_Transformer(tmp, origin, "i")
verifier = BoogieVerifier(
    transformer.fileName,
    origin,
    learner="dt_penalty",
    varlist=extract_variables_from_bpl(origin),
)
verifier.ensure_varlist_contains("i")
verifier.timeout = 20
verifier.GenerateConcreteBplFile(loop_bound)
transformer.GenerateConcreteBplFile(1, withinv=True)
ret, invariant, counterexample = verifier.run_verification(transformer.K_fileName)
print("lift_smoke_result", ret)
if ret != 1:
    raise SystemExit(1)
PY'
