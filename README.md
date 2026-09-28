# Deterministic AI Framework

Schema-first, self-healing AI infrastructure for production systems.

## Architecture status

This repository is being rebuilt in controlled steps as a deterministic control and governance layer around probabilistic AI systems.

See the project architecture specification from Step 01 for the governing design.

## Development

The project uses a modern Python package layout:

- `src/deterministic/` — package source
- `tests/` — automated tests
- `examples/` — reference examples
- `docs/` — architecture and governance documentation (added in later steps)

Install the package in development mode:

```bash
python -m pip install -e ".[dev]"
pytest
```

The existing prototype files are intentionally preserved while the framework is rebuilt. They will only be removed or replaced in a later step when their behavior has been migrated and tested.

## Status

Step 02 establishes the repository foundation. Core framework behavior is not yet considered production-ready.
