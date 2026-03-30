# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
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

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import (
        _utilities as _utilities,
        _validator as _validator,
        constants as constants,
        docker as docker,
        domains as domains,
        files as files,
        models as models,
        protocols as protocols,
        typings as typings,
        utilities as utilities,
        validator as validator,
    )
    from flext_tests._utilities import matchers as matchers
    from flext_tests._utilities._payload import (
        FlextTestsPayloadUtilities as FlextTestsPayloadUtilities,
        deep_match as deep_match,
        length_validate as length_validate,
        to_config_map_value as to_config_map_value,
        to_normalized_value as to_normalized_value,
        to_payload as to_payload,
    )
    from flext_tests._utilities.matchers import (
        FlextTestsMatchersUtilities as FlextTestsMatchersUtilities,
        tm as tm,
    )
    from flext_tests._validator import (
        bypass as bypass,
        imports as imports,
        layer as layer,
        settings as settings,
        tests as tests,
        types as types,
    )
    from flext_tests._validator.bypass import (
        FlextValidatorBypass as FlextValidatorBypass,
    )
    from flext_tests._validator.imports import (
        FlextValidatorImports as FlextValidatorImports,
    )
    from flext_tests._validator.layer import FlextValidatorLayer as FlextValidatorLayer
    from flext_tests._validator.models import (
        FlextValidatorModels as FlextValidatorModels,
        vm as vm,
    )
    from flext_tests._validator.settings import (
        FlextValidatorSettings as FlextValidatorSettings,
    )
    from flext_tests._validator.tests import FlextValidatorTests as FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes as FlextValidatorTypes
    from flext_tests.constants import (
        FlextTestsConstants as FlextTestsConstants,
        FlextTestsConstants as c,
    )
    from flext_tests.docker import FlextTestsDocker as FlextTestsDocker, tk as tk
    from flext_tests.domains import FlextTestsDomains as FlextTestsDomains, td as td
    from flext_tests.files import FlextTestsFiles as FlextTestsFiles, tf as tf
    from flext_tests.models import (
        FlextTestsModels as FlextTestsModels,
        FlextTestsModels as m,
    )
    from flext_tests.protocols import (
        FlextTestsProtocols as FlextTestsProtocols,
        FlextTestsProtocols as p,
    )
    from flext_tests.typings import (
        FlextTestsTypes as FlextTestsTypes,
        FlextTestsTypes as t,
    )
    from flext_tests.utilities import (
        FlextTestsUtilities as FlextTestsUtilities,
        FlextTestsUtilities as u,
    )
    from flext_tests.validator import (
        FlextTestsValidator as FlextTestsValidator,
        tv as tv,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextTestsConstants": ["flext_tests.constants", "FlextTestsConstants"],
    "FlextTestsDocker": ["flext_tests.docker", "FlextTestsDocker"],
    "FlextTestsDomains": ["flext_tests.domains", "FlextTestsDomains"],
    "FlextTestsFiles": ["flext_tests.files", "FlextTestsFiles"],
    "FlextTestsMatchersUtilities": [
        "flext_tests._utilities.matchers",
        "FlextTestsMatchersUtilities",
    ],
    "FlextTestsModels": ["flext_tests.models", "FlextTestsModels"],
    "FlextTestsPayloadUtilities": [
        "flext_tests._utilities._payload",
        "FlextTestsPayloadUtilities",
    ],
    "FlextTestsProtocols": ["flext_tests.protocols", "FlextTestsProtocols"],
    "FlextTestsTypes": ["flext_tests.typings", "FlextTestsTypes"],
    "FlextTestsUtilities": ["flext_tests.utilities", "FlextTestsUtilities"],
    "FlextTestsValidator": ["flext_tests.validator", "FlextTestsValidator"],
    "FlextValidatorBypass": ["flext_tests._validator.bypass", "FlextValidatorBypass"],
    "FlextValidatorImports": [
        "flext_tests._validator.imports",
        "FlextValidatorImports",
    ],
    "FlextValidatorLayer": ["flext_tests._validator.layer", "FlextValidatorLayer"],
    "FlextValidatorModels": ["flext_tests._validator.models", "FlextValidatorModels"],
    "FlextValidatorSettings": [
        "flext_tests._validator.settings",
        "FlextValidatorSettings",
    ],
    "FlextValidatorTests": ["flext_tests._validator.tests", "FlextValidatorTests"],
    "FlextValidatorTypes": ["flext_tests._validator.types", "FlextValidatorTypes"],
    "_utilities": ["flext_tests._utilities", ""],
    "_validator": ["flext_tests._validator", ""],
    "bypass": ["flext_tests._validator.bypass", ""],
    "c": ["flext_tests.constants", "FlextTestsConstants"],
    "constants": ["flext_tests.constants", ""],
    "d": ["flext_core", "d"],
    "deep_match": ["flext_tests._utilities._payload", "deep_match"],
    "docker": ["flext_tests.docker", ""],
    "domains": ["flext_tests.domains", ""],
    "e": ["flext_core", "e"],
    "files": ["flext_tests.files", ""],
    "h": ["flext_core", "h"],
    "imports": ["flext_tests._validator.imports", ""],
    "layer": ["flext_tests._validator.layer", ""],
    "length_validate": ["flext_tests._utilities._payload", "length_validate"],
    "m": ["flext_tests.models", "FlextTestsModels"],
    "matchers": ["flext_tests._utilities.matchers", ""],
    "models": ["flext_tests.models", ""],
    "p": ["flext_tests.protocols", "FlextTestsProtocols"],
    "protocols": ["flext_tests.protocols", ""],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "settings": ["flext_tests._validator.settings", ""],
    "t": ["flext_tests.typings", "FlextTestsTypes"],
    "td": ["flext_tests.domains", "td"],
    "tests": ["flext_tests._validator.tests", ""],
    "tf": ["flext_tests.files", "tf"],
    "tk": ["flext_tests.docker", "tk"],
    "tm": ["flext_tests._utilities.matchers", "tm"],
    "to_config_map_value": ["flext_tests._utilities._payload", "to_config_map_value"],
    "to_normalized_value": ["flext_tests._utilities._payload", "to_normalized_value"],
    "to_payload": ["flext_tests._utilities._payload", "to_payload"],
    "tv": ["flext_tests.validator", "tv"],
    "types": ["flext_tests._validator.types", ""],
    "typings": ["flext_tests.typings", ""],
    "u": ["flext_tests.utilities", "FlextTestsUtilities"],
    "utilities": ["flext_tests.utilities", ""],
    "validator": ["flext_tests.validator", ""],
    "vm": ["flext_tests._validator.models", "vm"],
    "x": ["flext_core", "x"],
}

_EXPORTS: Sequence[str] = [
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsMatchersUtilities",
    "FlextTestsModels",
    "FlextTestsPayloadUtilities",
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
    "_utilities",
    "_validator",
    "bypass",
    "c",
    "constants",
    "d",
    "deep_match",
    "docker",
    "domains",
    "e",
    "files",
    "h",
    "imports",
    "layer",
    "length_validate",
    "m",
    "matchers",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "settings",
    "t",
    "td",
    "tests",
    "tf",
    "tk",
    "tm",
    "to_config_map_value",
    "to_normalized_value",
    "to_payload",
    "tv",
    "types",
    "typings",
    "u",
    "utilities",
    "validator",
    "vm",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
