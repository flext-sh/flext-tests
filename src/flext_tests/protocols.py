"""Protocol definitions for FLEXT tests.

Provides FlextTestsProtocols, extending FlextProtocols with test-specific protocol
definitions. Currently serves as MRO parent for consumer project protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextProtocols

from flext_tests import t


class FlextTestsProtocols(FlextProtocols):
    """Protocol definitions for FLEXT tests - extends FlextProtocols.

    Architecture: Extends FlextProtocols with test-specific protocol definitions.
    All base protocols from FlextProtocols are available through inheritance pattern.
    Protocols cannot import models - only other protocols and types.
    """

    class Tests:
        """Test-specific protocol definitions namespace.

        Protocol classes are defined on-demand as consumer projects require them.
        Base protocols from FlextProtocols.* are inherited automatically.
        """


p = FlextTestsProtocols
__all__ = ["FlextTestsProtocols", "p"]
