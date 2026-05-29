# Docker Image

This directory stores a compressed, loadable Docker image:

```text
lift-repro-ubuntu20.04-tools.tar.gz
```

The loaded image tag is:

```text
lift-repro:ubuntu20.04-tools
```

## Load

From the repository root:

```bash
./scripts/load-docker-image.sh
```

The script verifies the archive checksum and runs `docker load`.

## Run

```bash
docker run -it --rm \
  -v "$PWD/LIFT:/root/LIFT" \
  -w /root/LIFT \
  lift-repro:ubuntu20.04-tools
```

The repository's `LIFT/` directory is mounted at `/root/LIFT`, matching the paths used by the experiment configuration.

## Validated Toolchain

- Ubuntu 20.04.3
- Python 3.8.10
- Mono 6.12.0.122
- Z3 4.8.9
- Boogie/ICE core retained in the image and also provided by `LIFT/ice`

The image intentionally excludes `experiment/`, `result_logs/`, and `experiment/baseline.scripts`. Use repository mounts and `data/baseline.scripts.tar.gz` for those payloads.

API keys are not included in the image. Set them at runtime if you want to run LLM-backed experiments.
