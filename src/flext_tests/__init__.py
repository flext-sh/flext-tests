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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x
    from flext_tests import (
        _utilities,
        _validator,
        constants,
        docker,
        domains,
        files,
        models,
        protocols,
        typings,
        utilities,
        validator,
    )
    from flext_tests._utilities import (
        FlextTestsMatchersUtilities,
        FlextTestsPayloadUtilities,
        deep_match,
        length_validate,
        matchers,
        tm,
        to_config_map_value,
        to_normalized_value,
        to_payload,
    )
    from flext_tests._validator import (
        FlextValidatorBypass,
        FlextValidatorImports,
        FlextValidatorLayer,
        FlextValidatorModels,
        FlextValidatorSettings,
        FlextValidatorTests,
        FlextValidatorTypes,
        bypass,
        imports,
        layer,
        settings,
        tests,
        types,
        vm,
    )
    from flext_tests.constants import FlextTestsConstants, FlextTestsConstants as c
    from flext_tests.docker import FlextTestsDocker, tk
    from flext_tests.domains import FlextTestsDomains, td
    from flext_tests.files import FlextTestsFiles, tf
    from flext_tests.models import FlextTestsModels, FlextTestsModels as m
    from flext_tests.protocols import FlextTestsProtocols, FlextTestsProtocols as p
    from flext_tests.typings import FlextTestsTypes, FlextTestsTypes as t
    from flext_tests.utilities import FlextTestsUtilities, FlextTestsUtilities as u
    from flext_tests.validator import FlextTestsValidator, tv

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_tests._utilities",
        "flext_tests._validator",
    ),
    {
        "FlextTestsConstants": "flext_tests.constants",
        "FlextTestsDocker": "flext_tests.docker",
        "FlextTestsDomains": "flext_tests.domains",
        "FlextTestsFiles": "flext_tests.files",
        "FlextTestsModels": "flext_tests.models",
        "FlextTestsProtocols": "flext_tests.protocols",
        "FlextTestsTypes": "flext_tests.typings",
        "FlextTestsUtilities": "flext_tests.utilities",
        "FlextTestsValidator": "flext_tests.validator",
        "_utilities": "flext_tests._utilities",
        "_validator": "flext_tests._validator",
        "c": ("flext_tests.constants", "FlextTestsConstants"),
        "constants": "flext_tests.constants",
        "d": "flext_core",
        "docker": "flext_tests.docker",
        "domains": "flext_tests.domains",
        "e": "flext_core",
        "files": "flext_tests.files",
        "h": "flext_core",
        "m": ("flext_tests.models", "FlextTestsModels"),
        "models": "flext_tests.models",
        "p": ("flext_tests.protocols", "FlextTestsProtocols"),
        "protocols": "flext_tests.protocols",
        "r": "flext_core",
        "s": "flext_core",
        "t": ("flext_tests.typings", "FlextTestsTypes"),
        "td": "flext_tests.domains",
        "tf": "flext_tests.files",
        "tk": "flext_tests.docker",
        "tv": "flext_tests.validator",
        "typings": "flext_tests.typings",
        "u": ("flext_tests.utilities", "FlextTestsUtilities"),
        "utilities": "flext_tests.utilities",
        "validator": "flext_tests.validator",
        "x": "flext_core",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
