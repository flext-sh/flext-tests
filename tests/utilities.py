"""Utilities for flext-tests tests."""

from __future__ import annotations

from typing import override

from flext_tests import FlextTestsUtilities, m, p, r, s, t

from .protocols import TestsFlextTestsProtocols


class TestsFlextTestsUtilities(FlextTestsUtilities):
    """Utilities for flext-tests tests."""

    class Tests(FlextTestsUtilities.Tests):
        """flext-tests test utilities namespace."""

        class MemoryEcho(TestsFlextTestsProtocols.Tests.Echo):
            """Real in-memory adapter of the ``Tests.Echo`` port (no mock/patch)."""

            @override
            def echo(self, value: str) -> str:
                """Return the upper-cased echo value."""
                return value.upper()

        class EchoService(s[str]):
            """Port-bearing service whose only collaborator is the echo port."""

            port: t.Port[TestsFlextTestsProtocols.Tests.Echo] = m.Field(
                exclude=True, description="Echo port the service delegates to."
            )

            def run(self) -> p.Result[str]:
                """Delegate the echo call to the port and return its result."""
                return r.ok(self.port.echo("hi"))


u = TestsFlextTestsUtilities

__all__: list[str] = ["TestsFlextTestsUtilities", "u"]
