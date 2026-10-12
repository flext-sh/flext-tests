"""Models for FLEXT tests.

Provides FlextTestsModels, extending m with test-specific model definitions
for factories, test data, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING

from flext_cli import FlextCliModels

from flext_tests._models import (
    FlextTestsFilesystemModelsMixin,
    FlextTestsFlextModelsBase,
    FlextTestsMakeModelsMixin,
    FlextTestsMatchersModelsMixin,
    FlextTestsWorkspaceCleanupModelsMixin,
)
from flext_tests._models.batch import FlextTestsBatchModelsMixin
from flext_tests._models.docker import FlextTestsDockerModelsMixin
from flext_tests._models.domains import FlextTestsDomainModelsMixin
from flext_tests._models.namespace import FlextTestsNamespaceModelsMixin
from flext_tests._models.validator import FlextTestsValidatorModelsMixin

# mid-init: the tail completion tolerates and defers — a None tail is legal
# until the models-end pass completes it.
if TYPE_CHECKING:
    from flext_tests import FlextTestsTypes

t: type[FlextTestsTypes] | None = None
with contextlib.suppress(ImportError):
    pass


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
