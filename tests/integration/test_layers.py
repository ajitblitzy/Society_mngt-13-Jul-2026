"""Integration tests for the cross-layer re-export contract of :mod:`society_mgmt`.

These tests replace the former JavaScript integration fixtures
(``society_mgmt_300k/tests/integration/file_10.js`` and ``file_21.js`` --
together 2,400 helper functions, ``mod_10_*`` and ``mod_21_*``, with zero
assertions) with a genuine, executable ``pytest`` suite.

The migrated package exposes a single source of truth,
:func:`society_mgmt.core.compute`, and each of the nine layer subpackages
re-exports that exact function object via ``from society_mgmt.core import
compute``. This suite asserts that Facade/re-export contract at the level of
object identity (not mere equality): for every layer,
``layer.compute is core.compute``.
"""

from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable
from typing import Protocol, cast

import pytest

import society_mgmt
from society_mgmt import core


class _LayerModule(Protocol):
    """Static contract for a ``society_mgmt`` layer subpackage namespace.

    Each layer subpackage re-exports the single canonical function and declares
    it as its public surface. Typing the imported module against this
    :class:`~typing.Protocol` (instead of a bare :class:`types.ModuleType`,
    whose attributes are ``Any``) makes ``module.compute`` and ``module.__all__``
    statically typed, so the assertions below are checked rather than silently
    typed as ``Any``.
    """

    __all__: list[str]
    compute: Callable[[float], float]


# The nine layer subpackages that must each re-export ``core.compute``.
LAYERS: list[str] = [
    "config",
    "controllers",
    "domain",
    "middleware",
    "models",
    "repositories",
    "routes",
    "services",
    "utils",
]

# Sample inputs exercising both parity branches of ``compute``: integer inputs
# (result even -> +10) and a non-integer (result odd -> +10 skipped).
SAMPLE_INPUTS: list[float] = [0, 3, 5, -1, 0.5]


def _import_layer(layer: str) -> _LayerModule:
    """Import and return the ``society_mgmt.<layer>`` subpackage, typed.

    The dynamically imported module is cast to :class:`_LayerModule` so its
    ``compute`` and ``__all__`` attributes carry concrete static types rather
    than ``Any``.
    """
    return cast(_LayerModule, importlib.import_module(f"society_mgmt.{layer}"))


@pytest.mark.parametrize("layer", LAYERS)
def test_layer_reexports_core_compute_identity(layer: str) -> None:
    """Each layer's ``compute`` IS the exact same object as ``core.compute``."""
    module = _import_layer(layer)
    assert module.compute is core.compute


@pytest.mark.parametrize("layer", LAYERS)
def test_layer_exposes_compute_in_all(layer: str) -> None:
    """Each layer declares ``compute`` as its public surface via ``__all__``."""
    module = _import_layer(layer)
    assert module.__all__ == ["compute"]


@pytest.mark.parametrize("layer", LAYERS)
@pytest.mark.parametrize("x", SAMPLE_INPUTS)
def test_layer_compute_matches_core(layer: str, x: float) -> None:
    """Each layer's ``compute`` yields identical results to ``core.compute``."""
    module = _import_layer(layer)
    assert module.compute(x) == core.compute(x)


def test_installed_layers_match_documented_exactly() -> None:
    """Enumerate the installed package and assert exactly the nine documented layers.

    Unlike a check of the hard-coded :data:`LAYERS` constant alone -- which
    would pass regardless of the package's real contents -- this introspects
    the *installed* ``society_mgmt`` package via :func:`pkgutil.iter_modules`
    and asserts the discovered subpackages equal exactly the nine documented
    layers. It therefore guards the single-source-of-truth topology (the AAP
    mandates exactly nine layer subpackages, with no extras): it fails if a
    tenth subpackage is added -- even one that violates the ``compute``
    re-export contract -- or if a documented layer is removed.
    """
    discovered = sorted(
        info.name for info in pkgutil.iter_modules(society_mgmt.__path__) if info.ispkg
    )
    assert discovered == sorted(LAYERS)
    assert len(discovered) == 9
