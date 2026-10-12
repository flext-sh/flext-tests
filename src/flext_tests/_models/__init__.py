# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._models.base import FlextTestsFlextModelsBase
    from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
    from flext_tests._models.make import FlextTestsMakeModelsMixin
    from flext_tests._models.matchers import FlextTestsMatchersModelsMixin
    from flext_tests._models.workspace_cleanup import (
        FlextTestsWorkspaceCleanupModelsMixin,
    )


__all__: tuple[str, ...] = (
    "FlextTestsFilesystemModelsMixin",
    "FlextTestsFlextModelsBase",
    "FlextTestsMakeModelsMixin",
    "FlextTestsMatchersModelsMixin",
    "FlextTestsWorkspaceCleanupModelsMixin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsFilesystemModelsMixin": ".filesystem",
        "FlextTestsFlextModelsBase": ".base",
        "FlextTestsMakeModelsMixin": ".make",
        "FlextTestsMatchersModelsMixin": ".matchers",
        "FlextTestsWorkspaceCleanupModelsMixin": ".workspace_cleanup",
    }),
    public_exports=__all__,
)
