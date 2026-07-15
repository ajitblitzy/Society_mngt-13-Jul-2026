"""Shared pytest fixtures and test data for the society_mgmt test suite.

Provides a small, canonical table of ``(input, expected)`` cases for
:func:`society_mgmt.core.compute`, reused across the unit tests. The cases
cover both parity branches:

* integer inputs, where ``6 * x`` is always even and ``10`` is added
  (e.g. ``compute(3) == 28``); and
* a non-integer input, where ``6 * x`` is odd and the ``+10`` is skipped
  (``compute(0.5) == 3.0``) -- proving the parity conditional is retained
  and not hard-coded.
"""

from __future__ import annotations

import pytest

# Canonical (input, expected) cases for society_mgmt.core.compute.
# Integer x -> 6*x + 10 (result even); non-integer 0.5 -> 3.0 (result odd, +10 skipped).
COMPUTE_CASES: list[tuple[float, float]] = [
    (0, 10),
    (3, 28),
    (5, 40),
    (-1, 4),
    (0.5, 3.0),
]


@pytest.fixture
def compute_cases() -> list[tuple[float, float]]:
    """Return the canonical ``(input, expected)`` cases for ``compute``."""
    return COMPUTE_CASES
