"""Base protocols for flext-tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flext_tests import p


from typing import Protocol, runtime_checkable

from flext_cli import p


class FlextTestsProtocolsBase:
    """Base protocols for flext-tests."""

    @runtime_checkable
    class ModelReader[ModelT: p.Model](Protocol):
        """Validate external content through a supplied model class capability."""

        __name__: str

        def model_validate(self, obj: p.AttributeProbe, /) -> ModelT:
            """Return the validated instance or raise the model owner's error."""
            ...

    @runtime_checkable
    class Payload(Protocol):
        """Structural data contract projected from the owning model."""

        kind: t.Tests.PayloadKind
        atom: t.Tests.PayloadAtom | t.Port[p.Model] | None
        items: t.Tests.PayloadItems[p.Tests.Payload]
        entries: t.Tests.PayloadEntries[p.Tests.Payload]

    @runtime_checkable
    class Entity(Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        value: p.Tests.Payload

    @runtime_checkable
    class Value(Protocol):
        """Structural data contract projected from the owning model."""

        data: str
        count: int


__all__: list[str] = ["FlextTestsProtocolsBase"]
