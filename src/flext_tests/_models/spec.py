"""Container-spec models for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import m, u

from flext_tests import t
from flext_tests._models.docker import FlextTestsDockerModelsMixin


class FlextTestsSpecModelsMixin:
    class ContainerSpec(m.Value):
        """Declarative spec of the containers one suite needs.

        One YAML document feeds both the pre-test CLI (`flext-tests docker
        ensure|verify|down --spec ...`) and the in-session plugin — a single
        SSOT so provisioning outside the pytest deadline and the in-session
        capability never diverge.
        """

        containers: Annotated[
            t.MutableMappingKV[str, FlextTestsDockerModelsMixin.ContainerConfig],
            u.Field(
                description=(
                    "Target name → container config; the target name is what "
                    "CLI --target and the in-session plugin resolve."
                ),
            ),
        ]
        initializer_command: Annotated[
            str | None,
            u.Field(
                description=(
                    "Optional shell command run once after ensure, receiving "
                    "the container environment readback as env vars."
                ),
            ),
        ] = None

