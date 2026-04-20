"""Constants for FLEXT tests.

Provides FlextTestsConstants, extending FlextCliConstants with test-specific constants
for Docker operations, container management, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import c

from flext_tests import (
    FlextTestsDockerConstantsMixin,
    FlextTestsFilesConstantsMixin,
    FlextTestsMatcherConstantsMixin,
    FlextTestsValidatorConstantsMixin,
)


class FlextTestsConstants(c):
    """Constants for FLEXT tests - extends FlextCliConstants.

    Architecture layer: Layer 0 foundation constants with test extensions.
    All base constants from FlextCliConstants are available through inheritance.
    """

    class Tests(
        FlextTestsDockerConstantsMixin,
        FlextTestsFilesConstantsMixin,
        FlextTestsMatcherConstantsMixin,
        FlextTestsValidatorConstantsMixin,
    ):
        """Test-specific constants namespace.

        All test-specific constants are organized under this namespace to clearly
        distinguish them from base FlextCliConstants. Access via c.Tests.*
        """


c = FlextTestsConstants

__all__: list[str] = ["FlextTestsConstants", "c"]
