"""Base protocols for flext-tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import t

if TYPE_CHECKING:
    from flext_cli import p

    from flext_tests._protocols import FlextTestsProtocolsPayload
    from flext_tests._typings import FlextTestsTypesBase


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

        kind: FlextTestsTypesBase.PayloadKind
        atom: FlextTestsTypesBase.PayloadAtom | t.Port[p.Model] | None
        items: FlextTestsTypesBase.PayloadItems[FlextTestsProtocolsPayload.Payload]
        entries: FlextTestsTypesBase.PayloadEntries[FlextTestsProtocolsPayload.Payload]

    @runtime_checkable
    class Entity(Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        value: FlextTestsProtocolsPayload.Payload

    @runtime_checkable
    class Value(Protocol):
        """Structural data contract projected from the owning model."""

        data: str
        count: int


__all__: list[str] = ["FlextTestsProtocolsBase"]
