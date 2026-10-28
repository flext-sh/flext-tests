# AUTO-GENERATED FILE — Regenerate with: make gen
"""Type system foundation for FLEXT tests.

Provides FlextTestsTypes, extending t with test-specific type definitions
for test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import t as flext_cli_t

from flext_tests._typings import (
    FlextTestsTypesBase,
    FlextTestsTypesDocker,
    FlextTestsTypesFiles,
    FlextTestsTypesMatchers,
    FlextTestsTypesPytest,
)


class FlextTestsTypes(flext_cli_t):
    """Type system foundation for FLEXT tests - extends t.

    Architecture: Extends t with test-specific type aliases and definitions.
    All base types from t are available through inheritance.
    """

    class Tests(
        FlextTestsTypesBase,
        FlextTestsTypesDocker,
        FlextTestsTypesFiles,
        FlextTestsTypesMatchers,
        FlextTestsTypesPytest,
    ):
        """Test-specific type definitions namespace.

        All test-specific types organized under t.Tests.* pattern.
        """


t = FlextTestsTypes
__all__: list[str] = ["FlextTestsTypes", "t"]
