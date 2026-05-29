# LIFT Lite Package

This zip archive is a size-reduced version of the LIFT artifact, intended to stay under common upload limits.

## What is included

- Core implementation: `code/` (including `code/Guess_Check/`)
- Main benchmarks used by LIFT: `experiment/benchmarks*`
- Core ICE/Boogie dependencies shipped with the artifact: `ice/popl16_artifact/` (Boogie, Z3, C5.0 data)
- Result processing scripts: `result_logs/data_script/`
- Experiment results: `result_logs/`
- Documentation: `README.md`, `result_logs/README.md`

## What is excluded (to reduce size)

- LEMUR baseline package and other baselines:
  - `experiment/baseline.scripts/` (this directory is large, especially `Lemur-program-verification`)
- Boogie source code (not needed to run the artifact with the shipped binaries):
  - `ice/popl16_artifact/Boogie/Source/`

## How to obtain excluded components

The excluded baseline packages (e.g., LEMUR integration / scripts) correspond to publicly available repositories and can be obtained separately by cloning their original sources.

If you need to reproduce baseline experiments, please refer to:
- `experiment/baseline.scripts/` documentation in the full artifact
- `result_logs/README.md` for the expected result file formats

## Notes

- LLM API keys are **not** included in the archive. Set them via environment variables at runtime as described in `code/Guess_Check/README.md`.
