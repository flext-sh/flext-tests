"""Protocols for FLEXT tests.

Provides FlextTestsProtocols, extending p and FlextCoreProtocols
with test-specific interfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_infra import p
from flext_tests._protocols.docker import FlextTestsDockerProtocolsMixin
from flext_tests._protocols.enforcement import FlextTestsEnforcementProtocolsMixin
from flext_tests._protocols.filesystem import FlextTestsFilesystemProtocolsMixin
from flext_tests._protocols.make import FlextTestsProtocolsMake
from flext_tests._protocols.matchers import FlextTestsMatcherProtocolsMixin
from flext_tests._protocols.valuefactory import FlextTestsValueFactoryProtocolsMixin
from flext_tests._protocols.workspace_cleanup import (
    FlextTestsWorkspaceCleanupProtocolsMixin,
)


class FlextTestsProtocols(p):
    """Protocols for FLEXT tests - extends p."""

    class Tests(
        FlextTestsDockerProtocolsMixin,
        FlextTestsEnforcementProtocolsMixin,
        FlextTestsFilesystemProtocolsMixin,
        # NOTE (multi-agent): expose Make model contracts through p.Tests.
        FlextTestsProtocolsMake,
        FlextTestsMatcherProtocolsMixin,
        FlextTestsValueFactoryProtocolsMixin,
        # NOTE (multi-agent): publish read-only cleanup contracts under p.Tests.
        FlextTestsWorkspaceCleanupProtocolsMixin,
    ):
        """Test-specific protocols namespace.

        All test protocols belong under this nested namespace to mirror
        models and constants. Access via p.Tests.*
        """


p = FlextTestsProtocols

__all__: list[str] = ["FlextTestsProtocols", "p"]
