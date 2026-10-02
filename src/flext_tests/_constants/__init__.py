# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._constants.base import FlextTestsConstantsBase
    from flext_tests._constants.data_cases import FlextTestsConstantsDataCases
    from flext_tests._constants.docker import FlextTestsConstantsDocker
    from flext_tests._constants.files import FlextTestsConstantsFiles
    from flext_tests._constants.kube import FlextTestsConstantsKube
    from flext_tests._constants.make import FlextTestsConstantsMake
    from flext_tests._constants.matcher import FlextTestsConstantsMatcher
    from flext_tests._constants.namespace import FlextTestsConstantsNamespace
    from flext_tests._constants.validator import FlextTestsConstantsValidator

__all__: tuple[str, ...] = (
    "FlextTestsConstantsBase",
    "FlextTestsConstantsDataCases",
    "FlextTestsConstantsDocker",
    "FlextTestsConstantsFiles",
    "FlextTestsConstantsKube",
    "FlextTestsConstantsMake",
    "FlextTestsConstantsMatcher",
    "FlextTestsConstantsNamespace",
    "FlextTestsConstantsValidator",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("FlextTestsConstantsBase",),
            ".data_cases": ("FlextTestsConstantsDataCases",),
            ".docker": ("FlextTestsConstantsDocker",),
            ".files": ("FlextTestsConstantsFiles",),
            ".kube": ("FlextTestsConstantsKube",),
            ".make": ("FlextTestsConstantsMake",),
            ".matcher": ("FlextTestsConstantsMatcher",),
            ".namespace": ("FlextTestsConstantsNamespace",),
            ".validator": ("FlextTestsConstantsValidator",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
