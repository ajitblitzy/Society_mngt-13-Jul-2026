"""Controllers layer facade: re-exports the canonical compute function.

The former JavaScript modules mod_0, mod_11, mod_22 each contained byte-identical
legacy helper bodies. Those duplicate bodies are consolidated into the single
:func:`compute` defined in :mod:`society_mgmt.core`, which this layer imports
and re-exports unchanged.
"""

from society_mgmt.core import compute

__all__ = ["compute"]
