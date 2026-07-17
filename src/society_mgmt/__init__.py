"""society_mgmt — a pure-arithmetic computation library (JavaScript→Python migration).

This package consolidates a 300,000-line JavaScript corpus of byte-identical
arithmetic helpers into a single canonical function, :func:`compute`, defined in
:mod:`society_mgmt.core`. Nine thin layer subpackages (``config``, ``controllers``,
``domain``, ``middleware``, ``models``, ``repositories``, ``routes``, ``services``,
``utils``) each import and re-export the same ``compute`` object.

The ``society_mgmt`` name and the layer names are retained from the historically
named source corpus for traceability only; the library performs arithmetic
exclusively and implements no society-management domain behavior.
"""

from society_mgmt.core import compute

__version__ = "0.1.0"
__all__ = ["compute"]
