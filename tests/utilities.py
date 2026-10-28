"""Utilities for flext-tests tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import Annotated, override

from flext_tests import FlextTestsServiceBase, FlextTestsUtilities
from tests import m, p, r, t


class TestsFlextTestsUtilities(FlextTestsUtilities):
    """Utilities for flext-tests tests."""

    class Tests(FlextTestsUtilities.Tests):
        """flext-tests test utilities namespace."""

        class MemoryEcho(p.Tests.Echo):
            """Real in-memory adapter of the ``Tests.Echo`` port (no mock/patch)."""

            @override
            def echo(self, value: str) -> str:
                """Return the upper-cased echo value."""
                return value.upper()

        class EchoService(FlextTestsServiceBase[str]):
            """Port-bearing service whose only collaborator is the echo port."""

            port: Annotated[
                t.Port[p.Tests.Echo],
                m.Field(
                    exclude=True,
                    description="Echo port the service delegates to.",
                ),
            ]

            def run(self) -> p.Result[str]:
                """Delegate the echo call to the port and return its result.

                Returns:
                    The resulting ``p.Result[str]``.

                """
                return r.ok(self.port.echo("hi"))


u = TestsFlextTestsUtilities

__all__: list[str] = ["TestsFlextTestsUtilities", "u"]
