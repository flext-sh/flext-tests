"""Models for FLEXT tests.

Provides FlextTestsModels, extending m with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m
from flext_tests import (
    FlextTestsBaseModelsMixin,
    FlextTestsBatchModelsMixin,
    FlextTestsDockerModelsMixin,
    FlextTestsFilesystemModelsMixin,
    FlextTestsMatchersModelsMixin,
    FlextTestsValidatorModelsMixin,
)


class FlextTestsModels(m):
    """Test models extending m with test-specific factory models."""

    class Tests(
        FlextTestsDockerModelsMixin,
        FlextTestsBaseModelsMixin,
        FlextTestsFilesystemModelsMixin,
        FlextTestsBatchModelsMixin,
        FlextTestsValidatorModelsMixin,
        FlextTestsMatchersModelsMixin,
    ):
        """Test-specific models namespace."""


m = FlextTestsModels

__all__ = ["FlextTestsModels", "m"]
