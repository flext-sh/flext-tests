"""Protocol definitions for flext-tests tests.

Provides TestsFlextTestsProtocols, extending TestsFlextProtocols with
flext-tests-specific protocol definitions.

Architecture:
- TestsFlextProtocols (flext_tests) = Generic protocols for all FLEXT projects
- TestsFlextTestsProtocols (tests/) = flext-tests-specific protocols extending TestsFlextProtocols

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols


class TestsFlextTestsProtocols(FlextTestsProtocols):
    """Protocol definitions for flext-tests tests - extends TestsFlextProtocols.

    Architecture: Extends TestsFlextProtocols with flext-tests-specific protocol
    definitions. All generic protocols from TestsFlextProtocols are available
    through inheritance.

    Rules:
    - NEVER redeclare protocols from TestsFlextProtocols
    - Only flext-tests-specific protocols allowed
    - All generic protocols come from TestsFlextProtocols
    """

    class Tests(FlextTestsProtocols.Tests):
        """flext-tests-specific protocol definitions namespace."""


p = TestsFlextTestsProtocols
__all__ = ["TestsFlextTestsProtocols", "p"]
