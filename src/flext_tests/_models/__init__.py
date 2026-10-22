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
    from flext_tests._models.docker import FlextTestsDockerModelsMixin
    from flext_tests._models.filesystem import FlextTestsFilesystemModelsMixin
    from flext_tests._models.matchers import FlextTestsMatchersModelsMixin
    from flext_tests._models.namespace import FlextTestsNamespaceModelsMixin
    from flext_tests._models.spec import FlextTestsSpecModelsMixin
    from flext_tests._models.tests_namespace import FlextTestsNamespace
    from flext_tests._models.validator import FlextTestsValidatorModelsMixin


__all__: tuple[str, ...] = (
    "FlextTestsDockerModelsMixin",
    "FlextTestsFilesystemModelsMixin",
    "FlextTestsFlextModelsBase",
    "FlextTestsMatchersModelsMixin",
    "FlextTestsNamespace",
    "FlextTestsNamespaceModelsMixin",
    "FlextTestsSpecModelsMixin",
    "FlextTestsValidatorModelsMixin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsDockerModelsMixin": ".docker",
        "FlextTestsFilesystemModelsMixin": ".filesystem",
        "FlextTestsFlextModelsBase": ".base",
        "FlextTestsMatchersModelsMixin": ".matchers",
        "FlextTestsNamespace": ".tests_namespace",
        "FlextTestsNamespaceModelsMixin": ".namespace",
        "FlextTestsSpecModelsMixin": ".spec",
        "FlextTestsValidatorModelsMixin": ".validator",
    }),
    public_exports=__all__,
)
