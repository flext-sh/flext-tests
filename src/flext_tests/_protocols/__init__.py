# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._protocols.base import FlextTestsProtocolsBase
    from flext_tests._protocols.docker import FlextTestsProtocolsDocker
    from flext_tests._protocols.enforcement import FlextTestsProtocolsEnforcement
    from flext_tests._protocols.fixture_trees import FlextTestsProtocolsFixtureTrees
    from flext_tests._protocols.matchers import FlextTestsProtocolsMatchers
    from flext_tests._protocols.payload import FlextTestsProtocolsPayload
    from flext_tests._protocols.valuefactory import FlextTestsProtocolsValueFactory


__all__: tuple[str, ...] = (
    "FlextTestsProtocolsBase",
    "FlextTestsProtocolsDocker",
    "FlextTestsProtocolsEnforcement",
    "FlextTestsProtocolsFixtureTrees",
    "FlextTestsProtocolsMatchers",
    "FlextTestsProtocolsPayload",
    "FlextTestsProtocolsValueFactory",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsProtocolsDocker": ".docker",
        "FlextTestsProtocolsEnforcement": ".enforcement",
        "FlextTestsProtocolsFixtureTrees": ".fixture_trees",
        "FlextTestsProtocolsMatchers": ".matchers",
        "FlextTestsProtocolsPayload": ".payload",
        "FlextTestsProtocolsBase": ".base",
        "FlextTestsProtocolsValueFactory": ".valuefactory",
    }),
    public_exports=__all__,
)
