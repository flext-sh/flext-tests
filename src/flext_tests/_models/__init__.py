# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._models.base import FlextTestsBaseModelsMixin
    from flext_tests._models.batch import FlextTestsBatchModelsMixin
    from flext_tests._models.docker import FlextTestsDockerModelsMixin
    from flext_tests._models.domains import FlextTestsDomainModelsMixin
    from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
    from flext_tests._models.make import FlextTestsMakeModelsMixin
    from flext_tests._models.matchers import FlextTestsMatchersModelsMixin
    from flext_tests._models.namespace import FlextTestsNamespaceModelsMixin
    from flext_tests._models.spec import FlextTestsSpecModelsMixin
    from flext_tests._models.validator import FlextTestsValidatorModelsMixin
    from flext_tests._models.workspace_cleanup import (
        FlextTestsWorkspaceCleanupModelsMixin,
    )


__all__: tuple[str, ...] = (
    "FlextTestsBaseModelsMixin",
    "FlextTestsBatchModelsMixin",
    "FlextTestsDockerModelsMixin",
    "FlextTestsDomainModelsMixin",
    "FlextTestsFilesystemModelsMixin",
    "FlextTestsMakeModelsMixin",
    "FlextTestsMatchersModelsMixin",
    "FlextTestsNamespaceModelsMixin",
    "FlextTestsSpecModelsMixin",
    "FlextTestsValidatorModelsMixin",
    "FlextTestsWorkspaceCleanupModelsMixin",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("FlextTestsBaseModelsMixin",),
            ".batch": ("FlextTestsBatchModelsMixin",),
            ".docker": ("FlextTestsDockerModelsMixin",),
            ".domains": ("FlextTestsDomainModelsMixin",),
            ".filesystem": ("FlextTestsFilesystemModelsMixin",),
            ".make": ("FlextTestsMakeModelsMixin",),
            ".matchers": ("FlextTestsMatchersModelsMixin",),
            ".namespace": ("FlextTestsNamespaceModelsMixin",),
            ".spec": ("FlextTestsSpecModelsMixin",),
            ".validator": ("FlextTestsValidatorModelsMixin",),
            ".workspace_cleanup": ("FlextTestsWorkspaceCleanupModelsMixin",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
