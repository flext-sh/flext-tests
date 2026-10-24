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
    from flext_tests._protocols.docker import FlextTestsDockerProtocolsMixin
    from flext_tests._protocols.enforcement import FlextTestsEnforcementProtocolsMixin
    from flext_tests._protocols.fixture_trees import (
        FlextTestsFixtureTreesProtocolsMixin,
    )
    from flext_tests._protocols.matchers import FlextTestsMatchersProtocolsMixin
    from flext_tests._protocols.payload import FlextTestsPayloadProtocolsMixin
    from flext_tests._protocols.valuefactory import FlextTestsValueFactoryProtocolsMixin


__all__: tuple[str, ...] = (
    "FlextTestsDockerProtocolsMixin",
    "FlextTestsEnforcementProtocolsMixin",
    "FlextTestsFixtureTreesProtocolsMixin",
    "FlextTestsMatchersProtocolsMixin",
    "FlextTestsPayloadProtocolsMixin",
    "FlextTestsProtocolsBase",
    "FlextTestsValueFactoryProtocolsMixin",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextTestsDockerProtocolsMixin": ".docker",
        "FlextTestsEnforcementProtocolsMixin": ".enforcement",
        "FlextTestsFixtureTreesProtocolsMixin": ".fixture_trees",
        "FlextTestsMatchersProtocolsMixin": ".matchers",
        "FlextTestsPayloadProtocolsMixin": ".payload",
        "FlextTestsProtocolsBase": ".base",
        "FlextTestsValueFactoryProtocolsMixin": ".valuefactory",
    }),
    public_exports=__all__,
)
