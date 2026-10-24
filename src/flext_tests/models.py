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
    FlextTestsDockerModelsMixin,
    FlextTestsFilesystemModelsMixin,
    FlextTestsFlextModelsBase,
    FlextTestsMatchersModelsMixin,
    FlextTestsNamespace,
    FlextTestsNamespaceModelsMixin,
    FlextTestsSpecModelsMixin,
    FlextTestsValidatorModelsMixin,
)


class FlextTestsModels(FlextCliModels):
    """Test models extending m with test-specific factory models."""

    class Tests(
        FlextTestsFlextModelsBase,
        FlextTestsDockerModelsMixin,
        FlextTestsFilesystemModelsMixin,
        FlextTestsMatchersModelsMixin,
        FlextTestsNamespaceModelsMixin,
        FlextTestsSpecModelsMixin,
        FlextTestsValidatorModelsMixin,
        FlextTestsNamespace,
        FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin,
    ):
        """Test-specific models namespace."""


m = FlextTestsModels

__all__: list[str] = ["FlextTestsModels", "m"]
