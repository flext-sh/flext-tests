# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tests/_protocols/namespace
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_cli import p

    from flext_tests import c, t


class FlextTestsProtocolsNamespace:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class TestNamespace(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def token(self) -> str:
            """Lowercase namespace token (23 chars)."""
            ...

        @property
        def run_token(self) -> str:
            """Shared token of the whole pytest run."""
            ...

        @property
        def worker(self) -> str:
            """Worker identifier (master outside xdist)."""
            ...

        @property
        def checkout(self) -> str:
            """Checkout identity digest prefix."""
            ...

        @property
        def issued_at_ns(self) -> int:
            """Issue time in nanoseconds."""
            ...

        @property
        def root(self) -> t.NonEmptyStr:
            """Absolute checkout root path."""
            ...

    @runtime_checkable
    class HandlerConfigParams(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def handler_type(self) -> c.HandlerType | None:
            """Explicit handler type override."""
            ...

        @property
        def handler_mode(self) -> c.HandlerType | None:
            """Explicit handler mode override."""
            ...

        @property
        def command_timeout(self) -> int | None:
            """Explicit command timeout override."""
            ...

        @property
        def max_command_retries(self) -> int | None:
            """Explicit command retry-count override."""
            ...

        @property
        def metadata(self) -> p.Metadata | None:
            """Explicit handler metadata override."""
            ...


__all__: list[str] = [
    "FlextTestsProtocolsNamespace",
]
