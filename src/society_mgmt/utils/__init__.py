"""Utils layer facade.

Re-exports :func:`society_mgmt.core.compute`, consolidating former modules
mod_4, mod_15, mod_26, whose legacy helper bodies were byte-identical to one
another. The comment-only ``filler.js`` padding module is excluded.
"""

from society_mgmt.core import compute

__all__ = ["compute"]
