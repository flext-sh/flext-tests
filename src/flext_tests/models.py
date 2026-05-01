"""Models for FLEXT tests.

Provides FlextTestsModels, extending m with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import m
from flext_tests._models.base import FlextTestsBaseModelsMixin
from flext_tests._models.batch import FlextTestsBatchModelsMixin
from flext_tests._models.docker import FlextTestsDockerModelsMixin
from flext_tests._models.domains import FlextTestsDomainModelsMixin
from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
from flext_tests._models.matchers import FlextTestsMatchersModelsMixin
from flext_tests._models.validator import FlextTestsValidatorModelsMixin


class FlextTestsModels(m):
    """Test models extending m with test-specific factory models."""

    class Tests(
        FlextTestsDockerModelsMixin,
        FlextTestsBaseModelsMixin,
        FlextTestsDomainModelsMixin,
        FlextTestsFilesystemModelsMixin,
        FlextTestsBatchModelsMixin,
        FlextTestsValidatorModelsMixin,
        FlextTestsMatchersModelsMixin,
    ):
        """Test-specific models namespace."""


m = FlextTestsModels

__all__: list[str] = ["FlextTestsModels", "m"]
