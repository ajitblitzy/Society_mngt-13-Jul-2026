"""Unit tests for :func:`society_mgmt.core.compute`.

These are real, executable assertions that replace the 2,400 assertion-less
JavaScript fixture functions of the former ``society_mgmt_300k/tests/unit/``
(``file_9.js`` = ``mod_9_0``..``mod_9_1199`` and ``file_20.js`` =
``mod_20_0``..``mod_20_1199``). Each legacy helper computed
``r = x*1 + x*2 + x*3`` (i.e. ``6 * x``) and added ``10`` when ``r`` was even,
yet asserted nothing. This suite pins that behavior with genuine assertions
covering BOTH parity branches (even-result integer inputs and a non-integer
input where the ``+10`` is skipped).
"""

from __future__ import annotations

import pytest

from society_mgmt import compute as compute_root
from society_mgmt.core import compute
from tests.conftest import COMPUTE_CASES

# Integer inputs: 6*x is always even, so compute(x) == 6*x + 10 (parity taken).
INTEGER_INPUTS: list[int] = [0, 1, 2, 3, 5, -1, -4, 10, 100]


@pytest.mark.parametrize(("x", "expected"), COMPUTE_CASES)
def test_compute_canonical_cases(x: float, expected: float) -> None:
    """compute matches the canonical (input, expected) table exactly."""
    assert compute(x) == expected


@pytest.mark.parametrize("x", INTEGER_INPUTS)
def test_compute_integer_identity(x: int) -> None:
    """For integer x, 6*x is even, so compute(x) equals 6*x + 10."""
    assert compute(x) == 6 * x + 10


def test_compute_non_integer_parity_skipped() -> None:
    """Non-integer 0.5 yields odd 3.0, so the +10 branch is skipped."""
    assert compute(0.5) == 3.0


def test_compute_uses_fixture(compute_cases: list[tuple[float, float]]) -> None:
    """The shared compute_cases fixture drives the same assertions."""
    for x, expected in compute_cases:
        assert compute(x) == expected


def test_compute_root_reexport_is_core() -> None:
    """The package root re-exports the exact same compute object as core."""
    assert compute_root is compute
