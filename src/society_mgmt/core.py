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
    is simplified to a single multiplication (``6 * x``), and the dead
    per-module ``store`` array is dropped, while the observable result is
    preserved exactly.

    The parity conditional is deliberately **retained** (rather than being
    hard-coded to ``6 * x + 10``) so that behavior matches the original helpers
    for every numeric input. For an integer ``x`` the intermediate ``6 * x`` is
    always even, so the branch adds ``10`` (e.g. ``compute(3) == 28``). For a
    non-integer such as ``x = 0.5`` the intermediate ``3.0`` is odd, so the
    ``10`` is *not* added (``compute(0.5) == 3.0``).

    Args:
        x: The numeric input.

    Returns:
        ``6 * x + 10`` when ``6 * x`` is even, otherwise ``6 * x``.

    Examples:
        >>> compute(0)
        10
        >>> compute(3)
        28
        >>> compute(5)
        40
        >>> compute(0.5)
        3.0

    """
    r = 6 * x
    return r + 10 if r % 2 == 0 else r
