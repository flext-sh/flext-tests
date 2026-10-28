"""Test-namespace models for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import m

from flext_tests import c, t


class FlextTestsModelsNamespace:
    class TestNamespace(m.Value):
        """Collision-free namespace token for one test run and one worker.

        The token mixes a base36 epoch stamp, the checkout identity, the
        worker code, and random bytes, so parallel pytest processes on the
        same host (and reruns after a reseeding plugin) never share a
        namespace.
        """

        token: Annotated[
            str,
            m.Field(
                pattern=c.Tests.NAMESPACE_ID_PATTERN,
                description="Lowercase namespace token (23 chars).",
            ),
        ]
        run_token: Annotated[
            str,
            m.Field(description="Shared token of the whole pytest run."),
        ]
        worker: Annotated[
            str,
            m.Field(description="Worker identifier (master outside xdist)."),
        ]
        checkout: Annotated[
            str,
            m.Field(description="Checkout identity digest prefix."),
        ]
        issued_at_ns: Annotated[
            int,
            m.Field(ge=0, description="Issue time in nanoseconds."),
        ]
        root: Annotated[
            t.NonEmptyStr,
            m.Field(description="Absolute checkout root path."),
        ]

    class HandlerConfigParams(m.Value):
        """Optional handler configuration knobs for ``create_handler_config``."""

        handler_type: Annotated[
            c.HandlerType | None,
            m.Field(description="Explicit handler type override."),
        ] = None
        handler_mode: Annotated[
            c.HandlerType | None,
            m.Field(description="Explicit handler mode override."),
        ] = None
        command_timeout: Annotated[
            int | None,
            m.Field(description="Explicit command timeout override."),
        ] = None
        max_command_retries: Annotated[
            int | None,
            m.Field(description="Explicit command retry-count override."),
        ] = None
        metadata: Annotated[
            m.Metadata | None,
            m.Field(description="Explicit handler metadata override."),
        ] = None


__all__: list[str] = ["FlextTestsModelsNamespace"]
