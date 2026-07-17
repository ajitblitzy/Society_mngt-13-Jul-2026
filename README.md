# Society_mngt-13-Jul-2026

A small, pure-computation Python library exposing a single canonical function,
`compute(x)`. The package is the result of a JavaScript-to-Python refactor: a
300,000-line JavaScript corpus containing roughly 33,105 byte-identical helper
functions was consolidated into one typed, documented function, eliminating the
massive duplication and dead code that dominated the original source. The
library performs arithmetic only — it implements no society-management domain
behavior; the project name and the layer names are retained from the historical
source corpus purely for traceability.

## Overview

The library performs arithmetic only: there is no persistence, networking, I/O, or
society-management domain behavior despite the historical layer names carried over from
the source project. Its design follows a strict **single source of truth** — the
computation is defined exactly once, in `src/society_mgmt/core.py`, and each of the nine
layer subpackages (`config`, `controllers`, `domain`, `middleware`, `models`,
`repositories`, `routes`, `services`, `utils`) imports and re-exports that exact same
`compute` object.

### Behavior

`compute(x)` returns `6 * x`, and adds `10` when that result is even. The parity
conditional is retained (rather than hard-coded to `6 * x + 10`) so the behavior matches
the original helpers for every numeric input:

- For an **integer** input, `6 * x` is always even, so `compute(x) == 6 * x + 10`
  (for example, `compute(3) == 28`).
- For a **non-integer** input the intermediate result may be odd, in which case
  the `+ 10` is skipped (for example, `compute(0.5) == 3.0`).

## Requirements

- Python `>= 3.12`

The library has **no runtime dependencies**; `compute` uses only built-in
numeric operators.

## Installation

Create and activate a virtual environment, then install the package in editable
mode.

```bash
# Create a virtual environment
python -m venv .venv

# Activate it (POSIX: Linux / macOS)
source .venv/bin/activate

# Activate it (Windows: PowerShell / cmd)
.venv\Scripts\activate

# Install the package (runtime only)
pip install -e .

# Or install with the development/test tooling (pytest, ruff, mypy)
pip install -e ".[dev]"
```

## Usage

Import `compute` from the package root and call it with any number:

```python
from society_mgmt import compute

compute(0)    # -> 10
compute(3)    # -> 28
compute(5)    # -> 40
compute(0.5)  # -> 3.0  (non-integer: 6 * 0.5 == 3.0 is odd, so +10 is skipped)
```

Because every layer subpackage re-exports the identical function object, you can
import `compute` from any layer namespace and get exactly the same behavior:

```python
from society_mgmt.services import compute

compute(3)  # -> 28

# The layer re-export IS the same object as the canonical core function:
from society_mgmt import compute as core_compute
from society_mgmt.services import compute as services_compute
assert services_compute is core_compute  # True
```

## Project structure

The package uses the modern `src/` layout. `core.py` holds the only
implementation of the computation; each of the nine layer subpackages is a thin
facade whose `__init__.py` does `from society_mgmt.core import compute` and
declares `__all__ = ["compute"]`.

```text
Society_mngt-13-Jul-2026/          (repository root)
├── pyproject.toml                 (PEP 621 metadata; setuptools backend; tool config)
├── README.md                      (this file)
├── LICENSE                        (Apache-2.0 + license reconciliation note)
├── .gitignore                     (Python build/test/venv ignores)
├── src/
│   └── society_mgmt/              (importable package)
│       ├── __init__.py            (package init; __version__; re-exports compute)
│       ├── core.py                (single source of truth: compute(x))
│       ├── config/__init__.py     (re-exports compute)
│       ├── controllers/__init__.py (re-exports compute)
│       ├── domain/__init__.py     (re-exports compute)
│       ├── middleware/__init__.py (re-exports compute)
│       ├── models/__init__.py     (re-exports compute)
│       ├── repositories/__init__.py (re-exports compute)
│       ├── routes/__init__.py     (re-exports compute)
│       ├── services/__init__.py   (re-exports compute)
│       └── utils/__init__.py      (re-exports compute)
└── tests/
    ├── __init__.py
    ├── conftest.py                (shared parametrized fixtures / canonical cases)
    ├── unit/
    │   ├── __init__.py
    │   └── test_core.py           (real assertions against compute)
    └── integration/
        ├── __init__.py
        └── test_layers.py         (asserts each layer re-export is core.compute)
```

**Single-source-of-truth design.** No layer redefines the logic. `core.compute`
is the sole implementation, and the layer packages simply re-export it. As a
result, any future change to the computation is a one-line edit in `core.py`,
and the layer taxonomy retains structural meaning without duplicating code.

## Running tests

Install the development extras (which include the test runner), then run the
suite from the repository root:

```bash
pip install -e ".[dev]"
pytest
```

The unit suite (`tests/unit/test_core.py`) asserts `compute` against a canonical
table of `(input, expected)` cases and covers both parity branches. The
integration suite (`tests/integration/test_layers.py`) verifies the cross-layer
contract — that each of the nine layer subpackages re-exports the exact same
`compute` object as `society_mgmt.core`.

Two optional developer tools are also configured in `pyproject.toml` and
installed with the `dev` extras:

```bash
# Lint and format checks
ruff check .
ruff format --check .

# Static type checking
mypy src tests
```

## License

This project is licensed under the **Apache License, Version 2.0**; see the
[`LICENSE`](LICENSE) file for the full text. During the JavaScript-to-Python
migration a conflicting, incomplete legacy MIT license stub (formerly nested in
the removed source corpus) was found; it has been removed, and `LICENSE`
includes a short reconciliation note documenting this for maintainer awareness.
Apache-2.0 is the authoritative license for the project.
