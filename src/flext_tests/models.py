# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models for FLEXT tests.

Provides FlextTestsModels, extending m with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_tests._models import (
    FlextTestsModelsDocker,
    FlextTestsModelsFilesystem,
    FlextTestsModelsFlextBase,
    FlextTestsModelsMatchers,
    FlextTestsModelsNamespace,
    FlextTestsModelsSpec,
    FlextTestsModelsValidator,
)


class FlextTestsModels(FlextCliModels):
    """Test models extending m with test-specific factory models."""

    class Tests(
        FlextTestsModelsFlextBase,
        FlextTestsModelsDocker,
        FlextTestsModelsFilesystem,
        FlextTestsModelsMatchers,
        FlextTestsModelsNamespace,
        FlextTestsModelsSpec,
        FlextTestsModelsValidator,
    ):
        """Test-specific models namespace."""


m = FlextTestsModels
__all__: list[str] = ["FlextTestsModels", "m"]
