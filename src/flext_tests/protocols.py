# AUTO-GENERATED FILE — Regenerate with: make gen
"""Protocols for FLEXT tests.

Provides FlextTestsProtocols, extending p and FlextCoreProtocols
with test-specific interfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliProtocols

from flext_tests._protocols import (
    FlextTestsDockerProtocolsMixin,
    FlextTestsEnforcementProtocolsMixin,
    FlextTestsFixtureTreesProtocolsMixin,
    FlextTestsMatchersProtocolsMixin,
    FlextTestsPayloadProtocolsMixin,
    FlextTestsValueFactoryProtocolsMixin,
)


class FlextTestsProtocols(FlextCliProtocols):
    """Protocols for FLEXT tests - extends p."""

    class Tests(
        FlextTestsDockerProtocolsMixin,
        FlextTestsValueFactoryProtocolsMixin,
        # Owned payload and matcher capability contracts consumed by matchers.
        FlextTestsPayloadProtocolsMixin,
        FlextTestsMatchersProtocolsMixin,
        # NOTE (multi-agent): publish read-only cleanup contracts under p.Tests.
        FlextTestsEnforcementProtocolsMixin,
        FlextTestsFixtureTreesProtocolsMixin,
    ):
        """Test-specific protocols namespace.

        All test protocols belong under this nested namespace to mirror
        models and constants. Access via p.Tests.*
        """


p = FlextTestsProtocols

__all__: list[str] = ["FlextTestsProtocols", "p"]
