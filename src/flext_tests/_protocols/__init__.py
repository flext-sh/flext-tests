# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._protocols.base import FlextTestsProtocolsBase
    from flext_tests._protocols.docker import FlextTestsDockerProtocolsMixin
    from flext_tests._protocols.enforcement import FlextTestsEnforcementProtocolsMixin
    from flext_tests._protocols.matchers import FlextTestsMatchersProtocolsMixin
    from flext_tests._protocols.payload import FlextTestsPayloadProtocolsMixin
    from flext_tests._protocols.valuefactory import FlextTestsValueFactoryProtocolsMixin
    from flext_tests._protocols.workspace_cleanup import (
        FlextTestsWorkspaceCleanupProtocols,
    )

__all__: tuple[str, ...] = (
    "FlextTestsDockerProtocolsMixin",
    "FlextTestsEnforcementProtocolsMixin",
    "FlextTestsMatchersProtocolsMixin",
    "FlextTestsPayloadProtocolsMixin",
    "FlextTestsProtocolsBase",
    "FlextTestsValueFactoryProtocolsMixin",
    "FlextTestsWorkspaceCleanupProtocols",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("FlextTestsProtocolsBase",),
            ".docker": ("FlextTestsDockerProtocolsMixin",),
            ".enforcement": ("FlextTestsEnforcementProtocolsMixin",),
            ".matchers": ("FlextTestsMatchersProtocolsMixin",),
            ".payload": ("FlextTestsPayloadProtocolsMixin",),
            ".valuefactory": ("FlextTestsValueFactoryProtocolsMixin",),
            ".workspace_cleanup": ("FlextTestsWorkspaceCleanupProtocols",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
