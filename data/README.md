# Data Archives

This directory stores large data/tooling payloads that should not be baked into the Docker image.

- `baseline.scripts.tar.gz`: optional baseline tool package from the validated full container.

To unpack it into the source tree:

```bash
./scripts/unpack-data.sh
```

After extraction, the baseline directory will be available at:

```text
LIFT/experiment/baseline.scripts/
```

The Docker image does not need to contain this directory. When running experiments, mount the repository's `LIFT/` directory into the container at `/root/LIFT`.
