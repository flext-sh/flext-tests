# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._models.base import FlextTestsFlextModelsBase
    from flext_tests._models.batch import FlextTestsBatchModelsMixin
    from flext_tests._models.docker import FlextTestsDockerModelsMixin
    from flext_tests._models.domains import FlextTestsDomainModelsMixin
    from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
    from flext_tests._models.make import FlextTestsMakeModelsMixin
    from flext_tests._models.matchers import FlextTestsMatchersModelsMixin
    from flext_tests._models.namespace import FlextTestsNamespaceModelsMixin
    from flext_tests._models.spec import FlextTestsSpecModelsMixin
    from flext_tests._models.tests_namespace import FlextTestsNamespace
    from flext_tests._models.tests_namespace import FlextTestsNamespace
    from flext_tests._models.validator import FlextTestsValidatorModelsMixin
    from flext_tests._models.workspace_cleanup import (
        FlextTestsWorkspaceCleanupModelsMixin,
    )


__all__: tuple[str, ...] = (
    "FlextTestsBatchModelsMixin",
    "FlextTestsDockerModelsMixin",
    "FlextTestsDomainModelsMixin",
    "FlextTestsFilesystemModelsMixin",
    "FlextTestsFlextModelsBase",
    "FlextTestsMakeModelsMixin",
    "FlextTestsMatchersModelsMixin",
    "FlextTestsNamespace",
    "FlextTestsNamespace",
    "FlextTestsNamespaceModelsMixin",
    "FlextTestsSpecModelsMixin",
    "FlextTestsValidatorModelsMixin",
    "FlextTestsWorkspaceCleanupModelsMixin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsBatchModelsMixin": ".batch",
        "FlextTestsDockerModelsMixin": ".docker",
        "FlextTestsDomainModelsMixin": ".domains",
        "FlextTestsFilesystemModelsMixin": ".filesystem",
        "FlextTestsFlextModelsBase": ".base",
        "FlextTestsMakeModelsMixin": ".make",
        "FlextTestsMatchersModelsMixin": ".matchers",
        "FlextTestsNamespace": ".tests_namespace",
        "FlextTestsNamespaceModelsMixin": ".namespace",
        "FlextTestsSpecModelsMixin": ".spec",
        "FlextTestsValidatorModelsMixin": ".validator",
        "FlextTestsWorkspaceCleanupModelsMixin": ".workspace_cleanup",
    }),
    public_exports=__all__,
)
