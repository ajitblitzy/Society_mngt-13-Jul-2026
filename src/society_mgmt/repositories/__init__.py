"""Repositories layer facade.

Re-exports :func:`society_mgmt.core.compute`, consolidating former modules
mod_7, mod_18, whose legacy helper bodies were byte-identical to one another.
"""

from society_mgmt.core import compute

__all__ = ["compute"]
