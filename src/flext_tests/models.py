"""Models for FLEXT tests.

Provides FlextTestsModels, extending m with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_infra import m

from ._models.base import FlextTestsBaseModelsMixin
from ._models.batch import FlextTestsBatchModelsMixin
from ._models.docker import FlextTestsDockerModelsMixin
from ._models.domains import FlextTestsDomainModelsMixin
from ._models.filesystem import FlextTestsFilesystemModelsMixin
from ._models.make import FlextTestsMakeModelsMixin
from ._models.matchers import FlextTestsMatchersModelsMixin
from ._models.validator import FlextTestsValidatorModelsMixin
from ._models.workspace_cleanup import FlextTestsWorkspaceCleanupModelsMixin


class FlextTestsModels(m):
    """Test models extending m with test-specific factory models."""

    class Tests(
        FlextTestsDockerModelsMixin,
        FlextTestsBaseModelsMixin,
        FlextTestsDomainModelsMixin,
        FlextTestsFilesystemModelsMixin,
        FlextTestsBatchModelsMixin,
        FlextTestsMakeModelsMixin,
        FlextTestsValidatorModelsMixin,
        FlextTestsMatchersModelsMixin,
        # NOTE (multi-agent): expose the approved typed cleanup contract through m.Tests.
        FlextTestsWorkspaceCleanupModelsMixin,
    ):
        """Test-specific models namespace."""


m = FlextTestsModels

__all__: list[str] = ["FlextTestsModels", "m"]
