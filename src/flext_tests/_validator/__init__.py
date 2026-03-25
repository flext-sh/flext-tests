# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Validator extensions for FLEXT architecture validation.

Internal module providing specialized validation methods.
Use via FlextTestsValidator (tv) in validator.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_tests._validator.bypass import FlextValidatorBypass
    from flext_tests._validator.imports import FlextValidatorImports
    from flext_tests._validator.layer import FlextValidatorLayer
    from flext_tests._validator.models import FlextValidatorModels, vm
    from flext_tests._validator.settings import FlextValidatorSettings
    from flext_tests._validator.tests import FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextValidatorBypass": ["flext_tests._validator.bypass", "FlextValidatorBypass"],
    "FlextValidatorImports": ["flext_tests._validator.imports", "FlextValidatorImports"],
    "FlextValidatorLayer": ["flext_tests._validator.layer", "FlextValidatorLayer"],
    "FlextValidatorModels": ["flext_tests._validator.models", "FlextValidatorModels"],
    "FlextValidatorSettings": ["flext_tests._validator.settings", "FlextValidatorSettings"],
    "FlextValidatorTests": ["flext_tests._validator.tests", "FlextValidatorTests"],
    "FlextValidatorTypes": ["flext_tests._validator.types", "FlextValidatorTypes"],
    "vm": ["flext_tests._validator.models", "vm"],
}

__all__ = [
    "FlextValidatorBypass",
    "FlextValidatorImports",
    "FlextValidatorLayer",
    "FlextValidatorModels",
    "FlextValidatorSettings",
    "FlextValidatorTests",
    "FlextValidatorTypes",
    "vm",
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
