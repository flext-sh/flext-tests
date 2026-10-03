"""Constants for FLEXT tests.

Provides FlextTestsConstants, extending FlextCliConstants with test-specific constants
for Docker operations, container management, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli import FlextCliConstants

from flext_tests._constants.data_cases import FlextTestsConstantsDataCases
from flext_tests._constants.docker import FlextTestsConstantsDocker
from flext_tests._constants.files import FlextTestsConstantsFiles
from flext_tests._constants.kube import FlextTestsConstantsKube
from flext_tests._constants.make import FlextTestsConstantsMake
from flext_tests._constants.matcher import FlextTestsConstantsMatcher
from flext_tests._constants.namespace import FlextTestsConstantsNamespace
from flext_tests._constants.validator import FlextTestsConstantsValidator

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsConstants(FlextCliConstants):
    """Constants for FLEXT tests - extends FlextCliConstants.

    Architecture layer: Layer 0 foundation constants with test extensions.
    All base constants from FlextCliConstants (and the FlextCore foundation
    beneath it) are available through inheritance.
    """

    class Tests(
        FlextCliConstants.Cli,
        FlextTestsConstantsDataCases,
        FlextTestsConstantsDocker,
        FlextTestsConstantsFiles,
        FlextTestsConstantsKube,
        FlextTestsConstantsMake,
        FlextTestsConstantsMatcher,
        FlextTestsConstantsNamespace,
        FlextTestsConstantsValidator,
    ):
        """Test-specific constants namespace.

        Composes the upstream CLI namespace with the test-specific parts so
        shared file/docker constants resolve through the MRO. Access via
        c.Tests.*
        """


c = FlextTestsConstants

__all__: t.VariadicTuple[str] = ("FlextTestsConstants", "c")
