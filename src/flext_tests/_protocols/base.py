"""Base protocols for flext-tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from collections.abc import Sequence

    from flext_cli import p

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
    class Payload(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def kind(self) -> FlextTestsTypesBase.PayloadKind:
            """Native value arm."""
            ...

        @property
        def atom(self) -> FlextTestsTypesBase.PayloadAtom | p.Model | None:
            """Native scalar or model instance; never a JSON dump."""
            ...

        @property
        def items(
            self,
        ) -> FlextTestsTypesBase.PayloadItems[FlextTestsProtocolsBase.Payload]:
            """Ordered children; kind retains the source collection."""
            ...

        @property
        def entries(
            self,
        ) -> FlextTestsTypesBase.PayloadEntries[FlextTestsProtocolsBase.Payload]:
            """String-keyed payload children."""
            ...

    @runtime_checkable
    class Entity(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        @property
        def name(self) -> str:
            """Entity display name."""
            ...

        @property
        def value(self) -> FlextTestsProtocolsBase.Payload:
            """Arbitrary serializable payload."""
            ...

    @runtime_checkable
    class Value(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def data(self) -> str:
            """Payload data string."""
            ...

        @property
        def count(self) -> int:
            """Occurrence counter."""
            ...


__all__: list[str] = ["FlextTestsProtocolsBase"]
