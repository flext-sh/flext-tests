# AUTO-GENERATED FILE — Regenerate with: make gen
"""Constants for FLEXT tests.

Provides FlextTestsConstants, extending FlextCliConstants with test-specific constants
for Docker operations, container management, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import c

from flext_tests._constants import (
    FlextTestsConstantsBase,
    FlextTestsConstantsDataCases,
    FlextTestsConstantsDocker,
    FlextTestsConstantsFiles,
    FlextTestsConstantsMatcher,
    FlextTestsConstantsNamespace,
    FlextTestsConstantsPytest,
    FlextTestsConstantsValidator,
)


class FlextTestsConstants(c):
    """Constants for FLEXT tests - extends FlextCliConstants.

    Architecture layer: Layer 0 foundation constants with test extensions.
    All base constants from FlextCliConstants (and the FlextCore foundation
    beneath it) are available through inheritance.
    """

    class Tests(
        FlextTestsConstantsBase,
        FlextTestsConstantsDataCases,
        FlextTestsConstantsDocker,
        FlextTestsConstantsFiles,
        FlextTestsConstantsMatcher,
        FlextTestsConstantsNamespace,
        FlextTestsConstantsPytest,
        FlextTestsConstantsValidator,
        c.Cli,
    ):
        """Test-specific constants namespace.

        Composes the upstream CLI namespace with the test-specific parts so
        shared file/docker constants resolve through the MRO. Access via
        c.Tests.*
        """


c = FlextTestsConstants
__all__: list[str] = ["FlextTestsConstants", "c"]
