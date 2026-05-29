# LIFT Artifact

This repository packages the LIFT source artifact, an optional baseline data archive, and a prebuilt Docker environment image for reproducing the paper experiments.

## Contents

- `LIFT/`: source code, core benchmarks, ICE/Boogie dependencies, result logs, and result scripts.
- `docker/`: compressed Docker image archive plus SHA256 checksum.
- `data/`: optional large data/tooling archives, currently `baseline.scripts.tar.gz`.
- `scripts/load-docker-image.sh`: verifies and loads the Docker image.
- `scripts/unpack-data.sh`: unpacks optional baseline data into `LIFT/experiment/`.
- `scripts/run-smoke-test.sh`: runs a no-LLM smoke test through LIFT's transform and Boogie verification path.

## Clone Options

### Code-only clone

Use this when you want to inspect or modify the code and configure the environment yourself:

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone https://github.com/prouzan/LIFT_Artifact.git LIFT-Artifact
cd LIFT-Artifact
```

The Docker image and baseline archive remain as lightweight Git LFS pointer files until explicitly pulled.

### Full clone with Docker image and baseline archive

Use this when you want the source plus the prebuilt Docker image and optional baseline package:

```bash
git lfs install
git clone https://github.com/prouzan/LIFT_Artifact.git LIFT-Artifact
cd LIFT-Artifact
git lfs pull --include="docker/*.tar.gz,data/*.tar.gz"
./scripts/load-docker-image.sh
./scripts/unpack-data.sh
```

GitHub's normal Git object limit is 100 MB and Git LFS has account quotas. The Docker image and baseline archive are tracked through Git LFS so lightweight clones can skip them. For long-term archival, consider mirroring the same archives to Zenodo, OSF, or an institutional artifact store.

## Docker Usage

After loading the image:

```bash
docker run -it --rm \
  -v "$PWD/LIFT:/root/LIFT" \
  -w /root/LIFT \
  lift-repro:ubuntu20.04-tools
```

Inside the container:

```bash
cd /root/LIFT
python3 code/Guess_Check/Check_loop_bound_newiter.py -c code/Guess_Check/config.yaml
```

The image does not include API keys. Set them at runtime before LLM-backed experiments:

```bash
export DPSK_API_KEY="..."
export DPSK_API_BASE="..."
export GEMINI_API_KEY="..."
export GEMINI_API_BASE="..."
```

The Docker image is intentionally environment-focused: it keeps the configured system/Python/Mono toolchain and Boogie/ICE core, but does not bake in benchmark data, result logs, or baseline packages. Mount this repository's `LIFT/` directory at `/root/LIFT` so experiments see the expected paths.

## Smoke Test

After loading the image, run:

```bash
./scripts/run-smoke-test.sh
```

The smoke test does not call an LLM. It injects a known loop bound for a small benchmark and verifies that LIFT's Boogie generation and ICE/Boogie checking path returns `1 verified, 0 errors`.

## Rebuilding The Docker Image

The checked-in image was prepared from the verified container `lift-repro:ubuntu20.04-full`. The important runtime components are:

- Ubuntu 20.04.3
- Python 3.8.10
- Mono 6.12.0.122
- Z3 4.8.9
- Boogie binaries in `LIFT/ice/popl16_artifact/Boogie/Binaries`
- C5.0/ICE dependencies in `LIFT/ice/popl16_artifact`

For code-only reproduction, follow the setup instructions in `LIFT/README.md`.

## Notes For Maintainers

- Do not commit API keys or local editor/agent state.
- Keep large archives in Git LFS.
- If publishing to GitHub, confirm your account's Git LFS quota before pushing the Docker image and baseline archive.
