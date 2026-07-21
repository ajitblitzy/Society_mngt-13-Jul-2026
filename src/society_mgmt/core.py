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

:func:`compute` accepts only the exact built-in numeric types ``int``,
``float`` and ``bool``; every other value is rejected with a :class:`TypeError`
*before* any arithmetic runs (see the function docstring for the rationale).
"""

__all__ = ["compute"]

# The exact built-in numeric types accepted by :func:`compute`. Membership is
# tested by *exact type identity* (via :func:`type`), not :func:`isinstance`, so
# that subclasses -- which may override ``__mul__``/``__rmul__`` and run arbitrary
# code during ``6 * x`` -- are rejected before any arithmetic operator can be
# dispatched. ``bool`` is listed explicitly because ``type(True) is bool`` (not
# ``int``), and both ``True`` and ``False`` are valid numeric inputs.
_SUPPORTED_TYPES: tuple[type, ...] = (int, float, bool)


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

    Only the exact built-in numeric types ``int``, ``float`` and ``bool`` are
    accepted. The input type is validated **before** any arithmetic is
    performed, so any other value -- ``str``, ``None``, ``complex``,
    ``Decimal``, ``Fraction``, a subclass of ``int``/``float``, or any custom
    object -- is rejected with a :class:`TypeError` *without* invoking a single
    operator dunder on it (for example ``__mul__`` or ``__rmul__``). This keeps
    the function pure and safe: an unsupported input cannot run side effects,
    return an attacker-chosen value, amplify memory usage, or block the call.

    Args:
        x: The numeric input. Must be an exact ``int``, ``float`` or ``bool``.

    Returns:
        ``6 * x + 10`` when ``6 * x`` is even, otherwise ``6 * x``.

    Raises:
        TypeError: If ``x`` is not an exact ``int``, ``float`` or ``bool``. The
            check runs before the arithmetic, so no operator method on ``x`` is
            ever invoked.

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
    if type(x) not in _SUPPORTED_TYPES:
        raise TypeError(
            f"compute() supports only int, float, and bool inputs; got {type(x).__name__!r}"
        )
    r = 6 * x
    return r + 10 if r % 2 == 0 else r
