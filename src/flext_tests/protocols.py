# AUTO-GENERATED FILE — Regenerate with: make gen
"""Protocols for FLEXT tests.

Provides FlextTestsProtocols, extending p and FlextCoreProtocols
with test-specific interfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias

from flext_cli import FlextCliProtocols

from flext_tests._protocols import (
    FlextTestsProtocolsBase,
    FlextTestsProtocolsDocker,
    FlextTestsProtocolsEnforcement,
    FlextTestsProtocolsFilesystem,
    FlextTestsProtocolsFixtureTrees,
    FlextTestsProtocolsHttp,
    FlextTestsProtocolsMatchers,
    FlextTestsProtocolsNamespace,
    FlextTestsProtocolsPayload,
    FlextTestsProtocolsSpec,
    FlextTestsProtocolsValidator,
    FlextTestsProtocolsValueFactory,
)


class FlextTestsProtocols(FlextCliProtocols):
    """Protocols for FLEXT tests - extends p."""

    class Tests(
        # Owned payload and matcher capability contracts consumed by matchers.
        # NOTE (multi-agent): publish read-only cleanup contracts under p.Tests.
        FlextTestsProtocolsBase,
        FlextTestsProtocolsDocker,
        FlextTestsProtocolsEnforcement,
        FlextTestsProtocolsFilesystem,
        FlextTestsProtocolsFixtureTrees,
        FlextTestsProtocolsHttp,
        FlextTestsProtocolsMatchers,
        FlextTestsProtocolsNamespace,
        FlextTestsProtocolsPayload,
        FlextTestsProtocolsSpec,
        FlextTestsProtocolsValidator,
        FlextTestsProtocolsValueFactory,
    ):
        """Test-specific protocols namespace.

        All test protocols belong under this nested namespace to mirror
        models and constants. Access via p.Tests.*
        """

        if TYPE_CHECKING:
            ModelReader: TypeAlias = FlextTestsProtocolsBase.ModelReader
            NodeFactory: TypeAlias = FlextTestsProtocolsEnforcement.NodeFactory
            MatchRule: TypeAlias = FlextTestsProtocolsMatchers.MatchRule
            Chain: TypeAlias = FlextTestsProtocolsMatchers.Chain
            EntityFactory: TypeAlias = FlextTestsProtocolsValueFactory.EntityFactory
            ValueFactory: TypeAlias = FlextTestsProtocolsValueFactory.ValueFactory


p = FlextTestsProtocols
__all__: list[str] = ["FlextTestsProtocols", "p"]
