# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_tests._utilities.docker import FlextTestsDocker, tk
    from flext_tests._utilities.domains import FlextTestsDomains, td
    from flext_tests._utilities.files import FlextTestsFiles, tf
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities, tm
    from flext_tests._utilities.validator import FlextTestsValidator, tv

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTestsDocker": ["flext_tests._utilities.docker", "FlextTestsDocker"],
    "FlextTestsDomains": ["flext_tests._utilities.domains", "FlextTestsDomains"],
    "FlextTestsFiles": ["flext_tests._utilities.files", "FlextTestsFiles"],
    "FlextTestsMatchersUtilities": [
        "flext_tests._utilities.matchers",
        "FlextTestsMatchersUtilities",
    ],
    "FlextTestsValidator": ["flext_tests._utilities.validator", "FlextTestsValidator"],
    "td": ["flext_tests._utilities.domains", "td"],
    "tf": ["flext_tests._utilities.files", "tf"],
    "tk": ["flext_tests._utilities.docker", "tk"],
    "tm": ["flext_tests._utilities.matchers", "tm"],
    "tv": ["flext_tests._utilities.validator", "tv"],
}

__all__ = [
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsMatchersUtilities",
    "FlextTestsValidator",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
