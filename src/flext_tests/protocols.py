"""Protocols for FLEXT tests.

Provides FlextTestsProtocols, extending FlextCliProtocols and FlextCoreProtocols
with test-specific interfaces.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import p as _cli_p
from flext_tests._protocols.valuefactory import FlextTestsValueFactoryProtocolsMixin


class FlextTestsProtocols(_cli_p):
    """Protocols for FLEXT tests - extends FlextCliProtocols."""

    class Tests(FlextTestsValueFactoryProtocolsMixin):
        """Test-specific protocols namespace.

        All test protocols belong under this nested namespace to mirror
        models and constants. Access via p.Tests.*
        """


p = FlextTestsProtocols

__all__ = ["FlextTestsProtocols", "p"]
