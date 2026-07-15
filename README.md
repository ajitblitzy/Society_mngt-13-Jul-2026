# Society_mngt-13-Jul-2026

A small, pure-computation Python library that exposes a single canonical function,
`compute(x)`.

## Overview

`society_mgmt` is the result of a JavaScript-to-Python refactor. The original corpus
was a ~300,000-line JavaScript project made up of roughly 33,105 byte-identical helper
functions with no module system, no packaging, and no real tests. The migration
collapsed all of that duplication into a single, well-typed, documented implementation
and packaged it as an installable Python library.

The library performs arithmetic only. There is no persistence, networking, I/O, or
society-management domain behavior despite the historical layer names carried over from
the source project. Its design follows a strict **single source of truth**: `compute`
is defined exactly once, in `society_mgmt.core`, and every layer subpackage imports and
re-exports that same function.

### Behavior

`compute(x)` evaluates `6 * x` in IEEE-754 double precision and adds `10` when that
result is even. The input is first normalized to a Python `float` (binary64), so the
function reproduces the original JavaScript `Number` semantics exactly and always
returns a `float`:

- For an integer `x`, `6 * x` is even, so the `+ 10` is applied (for example,
  `compute(3) == 28.0`). Very large magnitudes follow binary64 rounding, matching the
  original: values beyond `2 ** 53` are rounded to the nearest double before and after
  the `+ 10`.
- For a non-integer `x` the result may be odd, in which case the `+ 10` is skipped
  (for example, `compute(0.5) == 3.0`).

## Requirements

- **Python >= 3.12**

The library has **no runtime dependencies** — it uses only the Python standard library.
The optional development tooling (`pytest`, `ruff`, `mypy`) is declared as a `dev` extra
in `pyproject.toml`.

## Installation

Create and activate a virtual environment.

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Then install the package in editable mode. Add the `dev` extra to pull in the test and
code-quality tooling:

```bash
# Runtime install (no third-party dependencies)
pip install -e .

# Development install (adds pytest, ruff, mypy)
pip install -e ".[dev]"
```

## Usage

Import `compute` from the top-level package and call it with a number:

```python
from society_mgmt import compute

compute(0)  # -> 10.0
compute(3)  # -> 28.0
compute(5)  # -> 40.0
```

The same function is re-exported from every layer subpackage, so you can import it from
whichever namespace reads best at the call site — they all resolve to the identical
callable defined in `society_mgmt.core`:

```python
from society_mgmt.services import compute

compute(5)  # -> 40.0
```

Non-integer inputs follow the parity rule described in
[Behavior](#behavior) above:

```python
from society_mgmt import compute

compute(0.5)  # -> 3.0  (6 * 0.5 == 3.0 is odd, so +10 is skipped)
```

## Project structure

The package uses the modern `src/` layout:

```text
Society_mngt-13-Jul-2026/
├── pyproject.toml                     # PEP 621 metadata, setuptools backend, tool config
├── README.md                          # this file
├── LICENSE                            # Apache-2.0 (+ license reconciliation note)
├── .gitignore                         # Python build/test artifacts
├── src/
│   └── society_mgmt/
│       ├── __init__.py                # package init; __version__; re-exports compute
│       ├── core.py                    # single source of truth: compute(x)
│       ├── config/__init__.py         # re-exports compute
│       ├── controllers/__init__.py    # re-exports compute
│       ├── domain/__init__.py         # re-exports compute
│       ├── middleware/__init__.py     # re-exports compute
│       ├── models/__init__.py         # re-exports compute
│       ├── repositories/__init__.py   # re-exports compute
│       ├── routes/__init__.py         # re-exports compute
│       ├── services/__init__.py       # re-exports compute
│       └── utils/__init__.py          # re-exports compute
└── tests/
    ├── __init__.py
    ├── conftest.py                    # shared parametrized fixtures
    ├── unit/
    │   ├── __init__.py
    │   └── test_core.py               # asserts compute against closed-form values
    └── integration/
        ├── __init__.py
        └── test_layers.py             # asserts every layer re-export is core.compute
```

`core.compute` is the **only** implementation of the computation. The nine layer
subpackages (`config`, `controllers`, `domain`, `middleware`, `models`,
`repositories`, `routes`, `services`, `utils`) are thin namespaces that import and
re-export it via `__all__ = ["compute"]`, so the original domain taxonomy is preserved
without duplicating any logic.

## Running tests

Install the development extra, then run the suite with `pytest`:

```bash
pip install -e ".[dev]"
pytest
```

The unit suite (`tests/unit/test_core.py`) asserts `compute` against closed-form
expected values across both parity branches. The integration suite
(`tests/integration/test_layers.py`) asserts that each layer re-export is the same
callable as `society_mgmt.core.compute`.

Optional code-quality tooling is available through the same `dev` extra:

```bash
# Lint check
ruff check .

# Format check
ruff format --check .

# Static type check
mypy src
```

## License

This project is licensed under the **Apache License 2.0** — see the [`LICENSE`](LICENSE)
file for the full text. That file also carries a short reconciliation note: an earlier
revision of the repository contained a nested, incomplete MIT license stub, which has
been removed so that Apache-2.0 is the single, authoritative license for the project.
