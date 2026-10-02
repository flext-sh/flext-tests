"""Protocols for FLEXT tests.

Provides FlextTestsProtocols, extending p and FlextCoreProtocols
with test-specific interfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliProtocols

from flext_tests._protocols.docker import FlextTestsDockerProtocolsMixin
from flext_tests._protocols.enforcement import FlextTestsEnforcementProtocolsMixin
from flext_tests._protocols.matchers import FlextTestsMatchersProtocolsMixin
from flext_tests._protocols.payload import FlextTestsPayloadProtocolsMixin
from flext_tests._protocols.valuefactory import FlextTestsValueFactoryProtocolsMixin
from flext_tests._protocols.workspace_cleanup import FlextTestsWorkspaceCleanupProtocols


class FlextTestsProtocols(FlextCliProtocols):
    """Protocols for FLEXT tests - extends p."""

    class Tests(
        FlextTestsDockerProtocolsMixin,
        FlextTestsValueFactoryProtocolsMixin,
        # Owned payload and matcher capability contracts consumed by matchers.
        FlextTestsPayloadProtocolsMixin,
        FlextTestsMatchersProtocolsMixin,
        # NOTE (multi-agent): publish read-only cleanup contracts under p.Tests.
        FlextTestsWorkspaceCleanupProtocols,
        FlextTestsEnforcementProtocolsMixin,
    ):
        """Test-specific protocols namespace.

        All test protocols belong under this nested namespace to mirror
        models and constants. Access via p.Tests.*
        """


p = FlextTestsProtocols

__all__: list[str] = ["FlextTestsProtocols", "p"]
