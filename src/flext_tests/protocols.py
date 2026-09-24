"""Protocols for FLEXT tests.

Provides FlextTestsProtocols, extending p and FlextCoreProtocols
with test-specific interfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_infra import FlextInfraProtocols

from ._protocols.enforcement import FlextTestsEnforcementProtocolsMixin
from ._protocols.matchers import FlextTestsMatchersProtocolsMixin
from ._protocols.payload import FlextTestsPayloadProtocolsMixin
from ._protocols.valuefactory import FlextTestsValueFactoryProtocolsMixin
from ._protocols.workspace_cleanup import FlextTestsWorkspaceCleanupProtocols


class FlextTestsProtocols(FlextInfraProtocols):
    """Protocols for FLEXT tests - extends p."""

    class Tests(
        FlextTestsEnforcementProtocolsMixin,
        FlextTestsValueFactoryProtocolsMixin,
        # Owned payload and matcher capability contracts consumed by matchers.
        FlextTestsPayloadProtocolsMixin,
        FlextTestsMatchersProtocolsMixin,
        # NOTE (multi-agent): publish read-only cleanup contracts under p.Tests.
        FlextTestsWorkspaceCleanupProtocols,
    ):
        """Test-specific protocols namespace.

        All test protocols belong under this nested namespace to mirror
        models and constants. Access via p.Tests.*
        """


p = FlextTestsProtocols

__all__: list[str] = ["FlextTestsProtocols", "p"]
