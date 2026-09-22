"""Constants for FLEXT tests.

Provides FlextTestsConstants, extending FlextCliConstants with test-specific constants
for Docker operations, container management, and test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_cli import c as cli_c
from flext_infra import c as infra_c

from ._constants.data_cases import FlextTestsConstantsDataCases
from ._constants.docker import FlextTestsConstantsDocker
from ._constants.files import FlextTestsConstantsFiles
from ._constants.kube import FlextTestsConstantsKube
from ._constants.make import FlextTestsConstantsMake
from ._constants.matcher import FlextTestsConstantsMatcher
from ._constants.validator import FlextTestsConstantsValidator

if TYPE_CHECKING:
    from . import t


class FlextTestsConstants(cli_c, infra_c):
    """Constants for FLEXT tests - extends FlextCliConstants.

    Architecture layer: Layer 0 foundation constants with test extensions.
    All base constants from FlextCliConstants and FlextInfraConstants are
    available through inheritance.
    """

    class Tests(
        cli_c.Cli,
        FlextTestsConstantsDataCases,
        FlextTestsConstantsDocker,
        FlextTestsConstantsFiles,
        FlextTestsConstantsKube,
        FlextTestsConstantsMake,
        FlextTestsConstantsMatcher,
        FlextTestsConstantsValidator,
    ):
        """Test-specific constants namespace.

        Composes the upstream CLI namespace with the test-specific parts so
        shared file/docker constants resolve through the MRO. Access via
        c.Tests.*
        """


c = FlextTestsConstants

__all__: t.VariadicTuple[str] = ("FlextTestsConstants", "c")
