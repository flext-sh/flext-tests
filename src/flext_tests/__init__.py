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
    from flext_core import *

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
    from flext_tests._utilities import matchers
    from flext_tests._utilities._payload import *
    from flext_tests._utilities.matchers import *
    from flext_tests._validator import bypass, imports, layer, settings, tests, types
    from flext_tests._validator.bypass import *
    from flext_tests._validator.imports import *
    from flext_tests._validator.layer import *
    from flext_tests._validator.models import *
    from flext_tests._validator.settings import *
    from flext_tests._validator.tests import *
    from flext_tests._validator.types import *
    from flext_tests.constants import *
    from flext_tests.docker import *
    from flext_tests.domains import *
    from flext_tests.files import *
    from flext_tests.models import *
    from flext_tests.protocols import *
    from flext_tests.typings import *
    from flext_tests.utilities import *
    from flext_tests.validator import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextTestsConstants": "flext_tests.constants",
    "FlextTestsDocker": "flext_tests.docker",
    "FlextTestsDomains": "flext_tests.domains",
    "FlextTestsFiles": "flext_tests.files",
    "FlextTestsMatchersUtilities": "flext_tests._utilities.matchers",
    "FlextTestsModels": "flext_tests.models",
    "FlextTestsPayloadUtilities": "flext_tests._utilities._payload",
    "FlextTestsProtocols": "flext_tests.protocols",
    "FlextTestsTypes": "flext_tests.typings",
    "FlextTestsUtilities": "flext_tests.utilities",
    "FlextTestsValidator": "flext_tests.validator",
    "FlextValidatorBypass": "flext_tests._validator.bypass",
    "FlextValidatorImports": "flext_tests._validator.imports",
    "FlextValidatorLayer": "flext_tests._validator.layer",
    "FlextValidatorModels": "flext_tests._validator.models",
    "FlextValidatorSettings": "flext_tests._validator.settings",
    "FlextValidatorTests": "flext_tests._validator.tests",
    "FlextValidatorTypes": "flext_tests._validator.types",
    "_utilities": "flext_tests._utilities",
    "_validator": "flext_tests._validator",
    "bypass": "flext_tests._validator.bypass",
    "c": ["flext_tests.constants", "FlextTestsConstants"],
    "constants": "flext_tests.constants",
    "d": "flext_core",
    "deep_match": "flext_tests._utilities._payload",
    "docker": "flext_tests.docker",
    "domains": "flext_tests.domains",
    "e": "flext_core",
    "files": "flext_tests.files",
    "h": "flext_core",
    "imports": "flext_tests._validator.imports",
    "layer": "flext_tests._validator.layer",
    "length_validate": "flext_tests._utilities._payload",
    "m": ["flext_tests.models", "FlextTestsModels"],
    "matchers": "flext_tests._utilities.matchers",
    "models": "flext_tests.models",
    "p": ["flext_tests.protocols", "FlextTestsProtocols"],
    "protocols": "flext_tests.protocols",
    "r": "flext_core",
    "s": "flext_core",
    "settings": "flext_tests._validator.settings",
    "t": ["flext_tests.typings", "FlextTestsTypes"],
    "td": "flext_tests.domains",
    "tests": "flext_tests._validator.tests",
    "tf": "flext_tests.files",
    "tk": "flext_tests.docker",
    "tm": "flext_tests._utilities.matchers",
    "to_config_map_value": "flext_tests._utilities._payload",
    "to_normalized_value": "flext_tests._utilities._payload",
    "to_payload": "flext_tests._utilities._payload",
    "tv": "flext_tests.validator",
    "types": "flext_tests._validator.types",
    "typings": "flext_tests.typings",
    "u": ["flext_tests.utilities", "FlextTestsUtilities"],
    "utilities": "flext_tests.utilities",
    "validator": "flext_tests.validator",
    "vm": "flext_tests._validator.models",
    "x": "flext_core",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
