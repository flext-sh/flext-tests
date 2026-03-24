"""Protocol definitions for flext-tests tests.

Provides FlextTestsTestProtocols, extending FlextTestsProtocols with
flext-tests-specific protocol definitions.

Architecture:
- FlextTestsProtocols (flext_tests) = Generic protocols for all FLEXT projects
- FlextTestsTestProtocols (tests/) = flext-tests-specific protocols extending FlextTestsProtocols

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import FlextTestsProtocols


class FlextTestsTestProtocols(FlextTestsProtocols):
    """Protocol definitions for flext-tests tests - extends FlextTestsProtocols.

    Architecture: Extends FlextTestsProtocols with flext-tests-specific protocol
    definitions. All generic protocols from FlextTestsProtocols are available
    through inheritance.

    Rules:
    - NEVER redeclare protocols from FlextTestsProtocols
    - Only flext-tests-specific protocols allowed
    - All generic protocols come from FlextTestsProtocols
    """

    class Tests(FlextTestsProtocols.Tests):
        """flext-tests-specific protocol definitions namespace."""


p = FlextTestsTestProtocols
__all__ = ["FlextTestsTestProtocols", "p"]
