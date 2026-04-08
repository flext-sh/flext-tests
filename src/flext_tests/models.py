"""Models for FLEXT tests.

Provides FlextTestsModels, extending FlextModels with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextModels
from flext_tests import (
    FlextTestsBaseModelsMixin,
    FlextTestsBatchModelsMixin,
    FlextTestsDockerModelsMixin,
    FlextTestsFilesystemModelsMixin,
    FlextTestsMatchersModelsMixin,
    FlextTestsValidatorModelsMixin,
)


class FlextTestsModels(FlextModels):
    """Test models extending FlextModels with test-specific factory models."""

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
