"""society_mgmt — society management computation library (JavaScript→Python migration).

This package consolidates a 300,000-line JavaScript corpus of byte-identical
arithmetic helpers into a single canonical function, :func:`compute`, defined in
:mod:`society_mgmt.core`. Nine thin layer subpackages (``config``, ``controllers``,
``domain``, ``middleware``, ``models``, ``repositories``, ``routes``, ``services``,
``utils``) each import and re-export the same ``compute`` object.
"""

from society_mgmt.core import compute

__version__ = "0.1.0"
__all__ = ["compute"]
