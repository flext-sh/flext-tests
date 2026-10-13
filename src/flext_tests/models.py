"""Models for FLEXT tests.

Provides FlextTestsModels, extending m with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_tests._models.workspace_cleanup import (
    FlextTestsWorkspaceCleanupModelsMixin,
)
from flext_tests._models.batch import FlextTestsBatchModelsMixin
from flext_tests._models.docker import FlextTestsDockerModelsMixin
from flext_tests._models.domains import FlextTestsDomainModelsMixin
from flext_tests._models.namespace import FlextTestsNamespaceModelsMixin
from flext_tests._models.validator import FlextTestsValidatorModelsMixin
from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
from flext_tests._models.base import FlextTestsFlextModelsBase
from flext_tests._models.make import FlextTestsMakeModelsMixin
from flext_tests._models.matchers import FlextTestsMatchersModelsMixin


class FlextTestsModels(FlextCliModels):
    """Test models extending m with test-specific factory models."""

    class Tests(
        FlextTestsFlextModelsBase,
        FlextTestsFilesystemModelsMixin,
        FlextTestsMakeModelsMixin,
        FlextTestsMatchersModelsMixin,
        FlextTestsWorkspaceCleanupModelsMixin,
        FlextTestsDockerModelsMixin,
        FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin,
        FlextTestsDomainModelsMixin,
        FlextTestsNamespaceModelsMixin,
        FlextTestsBatchModelsMixin,
        FlextTestsValidatorModelsMixin,
    ):
        """Test-specific models namespace."""


m = FlextTestsModels

__all__: list[str] = ["FlextTestsModels", "m"]
