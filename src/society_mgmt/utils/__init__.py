"""Utils layer facade: re-exports the canonical compute function.

The former JavaScript modules mod_4, mod_15, mod_26 each contained byte-identical
legacy helper bodies. Those duplicate bodies are consolidated into the single
:func:`compute` defined in :mod:`society_mgmt.core`, which this layer imports
and re-exports unchanged. The comment-only filler.js padding module was excluded.
"""

from society_mgmt.core import compute

__all__ = ["compute"]
