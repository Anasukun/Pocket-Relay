# Development Guide

## Environment Setup
PocketRelay uses `uv` for dependency management.

```bash
# Clone the repository
git clone <repo-url>
cd PocketRelay

# Sync dependencies and create environment
uv sync
```

## Running Tests
Tests are written with `pytest`.

```bash
uv run pytest
```

## Code Quality
We use `ruff` for formatting and linting, and `mypy` for static typing.

```bash
uv run ruff format
uv run ruff check
uv run mypy src
```

## Adding Adapters
All adapters must implement the `AgentAdapter` protocol. Add new adapters to the `src/pocketrelay/adapters/` directory and ensure they pass the contract tests.
