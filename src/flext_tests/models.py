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

from flext_tests._models.base import FlextTestsFlextModelsBase
from flext_tests._models.batch import FlextTestsBatchModelsMixin
from flext_tests._models.docker import FlextTestsDockerModelsMixin
from flext_tests._models.domains import FlextTestsDomainModelsMixin
from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
from flext_tests._models.make import FlextTestsMakeModelsMixin
from flext_tests._models.matchers import FlextTestsMatchersModelsMixin
from flext_tests._models.namespace import FlextTestsNamespaceModelsMixin
from flext_tests._models.validator import FlextTestsValidatorModelsMixin
from flext_tests._models.workspace_cleanup import FlextTestsWorkspaceCleanupModelsMixin

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
        FlextTestsDockerModelsMixin,
        FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin,
        FlextTestsDomainModelsMixin,
        FlextTestsFilesystemModelsMixin,
        FlextTestsNamespaceModelsMixin,
        FlextTestsBatchModelsMixin,
        FlextTestsMakeModelsMixin,
        FlextTestsValidatorModelsMixin,
        FlextTestsMatchersModelsMixin,
        # NOTE (multi-agent): expose the approved typed cleanup contract
        # through m.Tests.
        FlextTestsWorkspaceCleanupModelsMixin,
    ):
        """Test-specific models namespace."""


m = FlextTestsModels

__all__: list[str] = ["FlextTestsModels", "m"]
