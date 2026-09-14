"""Read-only capability for owned native test payload trees."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, Self, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from flext_core import p
    from flext_tests import t


class FlextTestsPayloadProtocolsMixin:
    """Consumer-owned native payload access; no serialization capability required."""

    @runtime_checkable
    class NativeSequence(Protocol):
        """Native sequence capability at the ingress and comparison boundaries."""

        def __len__(self) -> int:
            """Return the number of native values."""
            ...

        def __iter__(self) -> Iterator[
            t.Tests.PayloadAtom
            | p.Model
            | FlextTestsPayloadProtocolsMixin.NativeSequence
            | FlextTestsPayloadProtocolsMixin.NativeMapping
            | None
        ]:
            """Iterate native values, not owned payload nodes."""
            ...

        def __getitem__(self, index: int) -> (
            t.Tests.PayloadAtom
            | p.Model
            | FlextTestsPayloadProtocolsMixin.NativeSequence
            | FlextTestsPayloadProtocolsMixin.NativeMapping
            | None
        ):
            """Read a native value by position."""
            ...

    @runtime_checkable
    class NativeMapping(Protocol):
        """Native mapping capability at the ingress and comparison boundaries."""

        def __len__(self) -> int:
            """Return the number of native entries."""
            ...

        def items(self) -> Iterable[
            tuple[
                str,
                t.Tests.PayloadAtom
                | p.Model
                | FlextTestsPayloadProtocolsMixin.NativeSequence
                | FlextTestsPayloadProtocolsMixin.NativeMapping
                | None,
            ]
        ]:
            """Read native entries without dumping model leaves."""
            ...

        def __getitem__(self, key: str) -> (
            t.Tests.PayloadAtom
            | p.Model
            | FlextTestsPayloadProtocolsMixin.NativeSequence
            | FlextTestsPayloadProtocolsMixin.NativeMapping
            | None
        ):
            """Read a native value by key."""
            ...

    @runtime_checkable
    class Payload(Protocol):
        """Inspect validated values without dumping or reconstructing model leaves."""

        @property
        def kind(self) -> t.Tests.PayloadKind:
            """Identify the native scalar or collection arm."""
            ...

        @property
        def atom(self) -> t.Tests.PayloadAtom | p.Model | None:
            """Read the unchanged native leaf."""
            ...

        @property
        def items(self) -> t.Tests.PayloadItems[Self]:
            """Read ordered children of a collection arm."""
            ...

        @property
        def entries(self) -> t.Tests.PayloadEntries[Self]:
            """Read children of a mapping arm."""
            ...
