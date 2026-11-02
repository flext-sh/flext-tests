# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tests/_protocols/namespace
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_tests import c, t

if TYPE_CHECKING:
    from flext_tests.protocols import p


class FlextTestsProtocolsNamespace:
    """Own the structural model contracts declared by this module."""

    @runtime_checkable
    class TestNamespace(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def token(self) -> str: ...
        @property
        def run_token(self) -> str: ...
        @property
        def worker(self) -> str: ...
        @property
        def checkout(self) -> str: ...
        @property
        def issued_at_ns(self) -> int: ...
        @property
        def root(self) -> t.NonEmptyStr: ...

    @runtime_checkable
    class HandlerConfigParams(Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def handler_type(self) -> c.HandlerType | None: ...
        @property
        def handler_mode(self) -> c.HandlerType | None: ...
        @property
        def command_timeout(self) -> int | None: ...
        @property
        def max_command_retries(self) -> int | None: ...
        @property
        def metadata(self) -> p.Metadata | None: ...


__all__: list[str] = [
    "FlextTestsProtocolsNamespace",
]
