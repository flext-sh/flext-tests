# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT Tests - Shared test utilities and fixtures package.

Provides comprehensive test infrastructure for the FLEXT ecosystem including
common test utilities, matchers, domain objects, factories, builders, Docker
container management, file operations, and integration with core FLEXT components.

Scope: Public API exports for all flext_tests modules including test utilities,
factories, builders, matchers, domain objects, Docker container management,
file operations, and re-exports of core FLEXT components for testing purposes.
All classes and utilities are designed for reuse across FLEXT test suites with
consistent patterns and comprehensive functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_tests import _utilities, _validator
    from flext_tests._utilities._payload import (
        deep_match,
        length_validate,
        to_config_map_value,
        to_normalized_value,
        to_payload,
    )
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities, tm
    from flext_tests._validator.bypass import FlextValidatorBypass
    from flext_tests._validator.imports import FlextValidatorImports
    from flext_tests._validator.layer import FlextValidatorLayer
    from flext_tests._validator.models import FlextValidatorModels, vm
    from flext_tests._validator.settings import FlextValidatorSettings
    from flext_tests._validator.tests import FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes
    from flext_tests.constants import FlextTestsConstants, FlextTestsConstants as c
    from flext_tests.docker import FlextTestsDocker, tk
    from flext_tests.domains import FlextTestsDomains, td
    from flext_tests.files import FlextTestsFiles, tf
    from flext_tests.models import FlextTestsModels, FlextTestsModels as m
    from flext_tests.protocols import (
        EntityFactory,
        FlextTestsProtocols,
        FlextTestsProtocols as p,
        ValueFactory,
    )
    from flext_tests.typings import FlextTestsTypes, FlextTestsTypes as t
    from flext_tests.utilities import FlextTestsUtilities, FlextTestsUtilities as u
    from flext_tests.validator import FlextTestsValidator, tv

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "EntityFactory": ("flext_tests.protocols", "EntityFactory"),
    "FlextTestsConstants": ("flext_tests.constants", "FlextTestsConstants"),
    "FlextTestsDocker": ("flext_tests.docker", "FlextTestsDocker"),
    "FlextTestsDomains": ("flext_tests.domains", "FlextTestsDomains"),
    "FlextTestsFiles": ("flext_tests.files", "FlextTestsFiles"),
    "FlextTestsMatchersUtilities": (
        "flext_tests._utilities.matchers",
        "FlextTestsMatchersUtilities",
    ),
    "FlextTestsModels": ("flext_tests.models", "FlextTestsModels"),
    "FlextTestsProtocols": ("flext_tests.protocols", "FlextTestsProtocols"),
    "FlextTestsTypes": ("flext_tests.typings", "FlextTestsTypes"),
    "FlextTestsUtilities": ("flext_tests.utilities", "FlextTestsUtilities"),
    "FlextTestsValidator": ("flext_tests.validator", "FlextTestsValidator"),
    "FlextValidatorBypass": ("flext_tests._validator.bypass", "FlextValidatorBypass"),
    "FlextValidatorImports": (
        "flext_tests._validator.imports",
        "FlextValidatorImports",
    ),
    "FlextValidatorLayer": ("flext_tests._validator.layer", "FlextValidatorLayer"),
    "FlextValidatorModels": ("flext_tests._validator.models", "FlextValidatorModels"),
    "FlextValidatorSettings": (
        "flext_tests._validator.settings",
        "FlextValidatorSettings",
    ),
    "FlextValidatorTests": ("flext_tests._validator.tests", "FlextValidatorTests"),
    "FlextValidatorTypes": ("flext_tests._validator.types", "FlextValidatorTypes"),
    "ValueFactory": ("flext_tests.protocols", "ValueFactory"),
    "_utilities": ("flext_tests._utilities", ""),
    "_validator": ("flext_tests._validator", ""),
    "c": ("flext_tests.constants", "FlextTestsConstants"),
    "d": ("flext_core", "d"),
    "deep_match": ("flext_tests._utilities._payload", "deep_match"),
    "e": ("flext_core", "e"),
    "h": ("flext_core", "h"),
    "length_validate": ("flext_tests._utilities._payload", "length_validate"),
    "m": ("flext_tests.models", "FlextTestsModels"),
    "p": ("flext_tests.protocols", "FlextTestsProtocols"),
    "r": ("flext_core", "r"),
    "s": ("flext_core", "s"),
    "t": ("flext_tests.typings", "FlextTestsTypes"),
    "td": ("flext_tests.domains", "td"),
    "tf": ("flext_tests.files", "tf"),
    "tk": ("flext_tests.docker", "tk"),
    "tm": ("flext_tests._utilities.matchers", "tm"),
    "to_config_map_value": ("flext_tests._utilities._payload", "to_config_map_value"),
    "to_normalized_value": ("flext_tests._utilities._payload", "to_normalized_value"),
    "to_payload": ("flext_tests._utilities._payload", "to_payload"),
    "tv": ("flext_tests.validator", "tv"),
    "u": ("flext_tests.utilities", "FlextTestsUtilities"),
    "vm": ("flext_tests._validator.models", "vm"),
    "x": ("flext_core", "x"),
}

__all__ = [
    "EntityFactory",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsMatchersUtilities",
    "FlextTestsModels",
    "FlextTestsProtocols",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidator",
    "FlextValidatorBypass",
    "FlextValidatorImports",
    "FlextValidatorLayer",
    "FlextValidatorModels",
    "FlextValidatorSettings",
    "FlextValidatorTests",
    "FlextValidatorTypes",
    "ValueFactory",
    "_utilities",
    "_validator",
    "c",
    "d",
    "deep_match",
    "e",
    "h",
    "length_validate",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "to_config_map_value",
    "to_normalized_value",
    "to_payload",
    "tv",
    "u",
    "vm",
    "x",
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
