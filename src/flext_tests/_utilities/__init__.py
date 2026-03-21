# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities, tm

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextTestsMatchersUtilities": (
        "flext_tests._utilities.matchers",
        "FlextTestsMatchersUtilities",
    ),
    "tm": ("flext_tests._utilities.matchers", "tm"),
}

__all__ = [
    "FlextTestsMatchersUtilities",
    "tm",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
