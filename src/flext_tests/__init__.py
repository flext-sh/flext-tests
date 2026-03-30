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

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if TYPE_CHECKING:
    from flext_tests._utilities import *
    from flext_tests._validator import *
    from flext_tests.constants import *
    from flext_tests.docker import *
    from flext_tests.domains import *
    from flext_tests.files import *
    from flext_tests.models import *
    from flext_tests.protocols import *
    from flext_tests.typings import *
    from flext_tests.utilities import *
    from flext_tests.validator import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
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
