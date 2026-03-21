# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_tests._utilities.docker import FlextTestsDockerUtilities, tk
    from flext_tests._utilities.files import FlextTestsFilesUtilities
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextTestsDockerUtilities": (
        "flext_tests._utilities.docker",
        "FlextTestsDockerUtilities",
    ),
    "FlextTestsFilesUtilities": (
        "flext_tests._utilities.files",
        "FlextTestsFilesUtilities",
    ),
    "FlextTestsMatchersUtilities": (
        "flext_tests._utilities.matchers",
        "FlextTestsMatchersUtilities",
    ),
    "tk": ("flext_tests._utilities.docker", "tk"),
}

__all__ = [
    "FlextTestsDockerUtilities",
    "FlextTestsFilesUtilities",
    "FlextTestsMatchersUtilities",
    "tk",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
