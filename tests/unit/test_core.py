"""Unit tests for :func:`society_mgmt.core.compute`.

These are real, executable assertions that replace the 2,400 assertion-less
JavaScript fixture functions of the former ``society_mgmt_300k/tests/unit/``
(``file_9.js`` = ``mod_9_0``..``mod_9_1199`` and ``file_20.js`` =
``mod_20_0``..``mod_20_1199``). Each legacy helper computed
``r = x*1 + x*2 + x*3`` (i.e. ``6 * x``) and added ``10`` when ``r`` was even,
yet asserted nothing. This suite pins that behavior with genuine assertions
covering BOTH parity branches (even-result integer inputs and a non-integer
input where the ``+10`` is skipped).

It also pins the input-safety contract: ``compute`` accepts only the exact
built-in numeric types ``int``, ``float`` and ``bool``, and rejects every other
value with a :class:`TypeError` *before* any arithmetic runs, so no operator
dunder on an unsupported input is ever invoked (regression coverage for a
custom ``__rmul__`` object and a hostile ``float`` subclass proving the hook
never fires).
"""

from __future__ import annotations

import pytest

from society_mgmt import compute as compute_root
from society_mgmt.core import compute
from tests.conftest import COMPUTE_CASES

# Integer inputs: 6*x is always even, so compute(x) == 6*x + 10 (parity taken).
INTEGER_INPUTS: list[int] = [0, 1, 2, 3, 5, -1, -4, 10, 100]

# Representative unsupported inputs. None is an exact int/float/bool, so each
# must be rejected with a TypeError before any arithmetic runs.
UNSUPPORTED_INPUTS: list[object] = [
    "3",
    None,
    [1, 2, 3],
    {"a": 1},
    (1, 2),
    b"bytes",
    complex(1, 2),
]


class _HostileRmul:
    """An object whose ``__rmul__`` records that it was invoked.

    If ``compute`` ever evaluated ``6 * x`` for an unsupported object, Python
    would dispatch this ``__rmul__`` (because ``int.__mul__`` returns
    ``NotImplemented`` for an unknown right operand), running the side effect
    and returning an attacker-chosen value. The input guard must reject the
    object first, so :attr:`invoked` must stay ``False``.
    """

    def __init__(self) -> None:
        self.invoked: bool = False

    def __rmul__(self, other: object) -> int:
        self.invoked = True
        return 0


class _HostileFloatSubclass(float):
    """A ``float`` subclass whose ``__rmul__`` must be unreachable via compute.

    Because it *is* a ``float`` subclass, an ``isinstance`` check would admit
    it; the exact-type guard rejects it. If the guard used ``isinstance``, the
    ``6 * x`` step would dispatch this ``__rmul__`` and fire the payload, so
    :attr:`fired` must stay ``False``.
    """

    fired: bool = False

    def __rmul__(self, other: object) -> float:
        _HostileFloatSubclass.fired = True
        return 0.0


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


def test_compute_rejects_hostile_rmul_object_without_firing_hook() -> None:
    """A custom object is rejected before its ``__rmul__`` payload can run.

    Regression for S9-01: ``compute`` must validate the input type before the
    ``6 * x`` multiplication, so a hostile ``__rmul__`` is never dispatched --
    no side effect, no attacker-chosen return value, and (since the hook is
    never entered) no possibility of an indefinite block.
    """
    hostile = _HostileRmul()
    with pytest.raises(TypeError):
        compute(hostile)  # type: ignore[arg-type]
    assert hostile.invoked is False


def test_compute_rejects_hostile_float_subclass_without_firing_hook() -> None:
    """A ``float`` subclass is rejected by exact-type check, hook never fires.

    Regression for S9-01: an ``isinstance`` guard would admit a ``float``
    subclass and then dispatch its overridden ``__rmul__`` during ``6 * x``.
    The exact-type guard rejects it first, so ``fired`` stays ``False``.
    """
    _HostileFloatSubclass.fired = False
    with pytest.raises(TypeError):
        compute(_HostileFloatSubclass(1.0))
    assert _HostileFloatSubclass.fired is False


@pytest.mark.parametrize("bad", UNSUPPORTED_INPUTS)
def test_compute_rejects_unsupported_types(bad: object) -> None:
    """Unsupported built-in types raise ``TypeError`` (no silent coercion)."""
    with pytest.raises(TypeError):
        compute(bad)  # type: ignore[arg-type]


def test_compute_recovers_after_rejected_input() -> None:
    """A valid call still works after an unsupported input was rejected."""
    with pytest.raises(TypeError):
        compute("not a number")  # type: ignore[arg-type]
    assert compute(3) == 28
