"""Core computation for the ``society_mgmt`` package.

This module is the **single source of truth** for the package's arithmetic. It
consolidates the 28,305 byte-identical helper functions from the former
JavaScript corpus (``society_mgmt_300k/src/**/*.js``) into one canonical, pure
function, :func:`compute`. Every layer subpackage (``controllers``,
``services``, ``routes``, ``models``, ``domain``, ``repositories``,
``middleware``, ``config`` and ``utils``) as well as the package root
re-export this exact function object, so the corpus-wide duplication collapses
to a single definition (DRY / single source of truth).

The module has no internal dependencies: it is the acyclic *sink* of the
package's dependency graph and relies solely on built-in numeric operators.
"""

__all__ = ["compute"]


def compute(x: float) -> float:
    """Return ``6 * x``, plus ``10`` when the result is even.

    This is the behavior-preserving Python port of the original JavaScript
    helper, whose body accumulated ``r = x*1 + x*2 + x*3`` (equivalent to
    ``6 * x``) and added ``10`` when ``r`` was even. The redundant accumulation
    is simplified to a single multiplication, and the dead per-module ``store``
    array is dropped, while the observable result is preserved exactly.

    Every original helper operated on JavaScript ``Number`` values, i.e.
    IEEE-754 binary64 floats. The input is therefore normalized with
    ``float(x)`` before the arithmetic, so the computation reproduces the
    source's ``Number`` semantics for *all* inputs -- including integers whose
    magnitude exceeds ``2 ** 53``, which are rounded to the nearest binary64
    exactly as JavaScript did rather than being evaluated with Python's
    arbitrary-precision integers. The ``6 * x`` simplification is safe in
    binary64: it is bit-identical to the original ``x*1 + x*2 + x*3``
    accumulation. Consequently :func:`compute` always returns a ``float``. (An
    ``int`` whose magnitude exceeds the binary64 range raises
    :class:`OverflowError` -- the sole point at which Python's integer domain
    extends beyond JavaScript's ``Number`` range.)

    The parity conditional is deliberately **retained** (rather than being
    hard-coded to ``6 * x + 10``) so that behavior matches the original helpers
    for every input. For an integer ``x`` the intermediate ``6 * x`` is even, so
    the branch adds ``10`` (e.g. ``compute(3) == 28.0``); above ``2 ** 53`` the
    ``+ 10`` may be rounded away exactly as in JavaScript (e.g.
    ``compute(9007199254740993) == 54043195528445960.0``). For a non-integer
    such as ``x = 0.5`` the intermediate ``3.0`` is odd, so the ``10`` is *not*
    added (``compute(0.5) == 3.0``).

    Args:
        x: The numeric input (``int`` or ``float``). Integer inputs are
            normalized to IEEE-754 binary64, matching JavaScript ``Number``.

    Returns:
        ``6 * x + 10`` when ``6 * x`` is even, otherwise ``6 * x``, as a
        ``float``.

    Examples:
        >>> compute(0)
        10.0
        >>> compute(3)
        28.0
        >>> compute(5)
        40.0
        >>> compute(0.5)
        3.0

    """
    r = 6 * float(x)
    return r + 10 if r % 2 == 0 else r
