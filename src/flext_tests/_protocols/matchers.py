"""Callable contracts over native matcher values.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_tests import t

if TYPE_CHECKING:
    from collections.abc import Callable

    from flext_tests._protocols.payload import FlextTestsProtocolsPayload
    from flext_tests._typings.matchers import FlextTestsTypesMatchers


class FlextTestsProtocolsMatchers(Protocol):
    """Structural matcher capabilities without recursive type aliases."""

    type MatcherOption = (
        FlextTestsProtocolsPayload.NativeMatchValue
        | FlextTestsProtocolsPayload.Payload
        | t.RegexPattern
        | type
        | tuple[type, ...]
        | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool]
        | Callable[
            [FlextTestsProtocolsPayload.NativeMatchValue],
            FlextTestsProtocolsPayload.NativeMatchValue,
        ]
        | Mapping[
            str | int,
            FlextTestsProtocolsPayload.NativeMatchValue
            | FlextTestsProtocolsPayload.Payload
            | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool],
        ]
        | FlextTestsProtocolsMatchers.MatcherCriteriaMapping
        | FlextTestsProtocolsMatchers.MatcherCriteriaSequence
        | Sequence[str]
        | FlextTestsTypesMatchers.LengthSpec
    )

    @runtime_checkable
    class MatcherCriteriaMapping(Protocol):
        """Read nested native matcher criteria independently of payload values."""

        def __len__(self) -> int:
            """Return the number of declared criteria."""
            ...

        def items(
            self,
        ) -> Iterable[tuple[str | int, FlextTestsProtocolsMatchers.MatcherOption]]:
            """Iterate selectors and their unchanged native criteria."""
            ...

    @runtime_checkable
    class MatcherCriteriaSequence(Protocol):
        """Read ordered native criteria without converting their operands."""

        def __len__(self) -> int:
            """Return the number of positional criteria."""
            ...

        def __iter__(self) -> Iterator[FlextTestsProtocolsMatchers.MatcherOption]:
            """Iterate the original criteria."""
            ...

        def __getitem__(
            self, index: int, /
        ) -> FlextTestsProtocolsMatchers.MatcherOption:
            """Read one positional criterion."""
            ...

    @runtime_checkable
    class MatchPredicate(Protocol):
        """Evaluate the native value a matcher criterion is applied to."""

        def __call__(
            self,
            value: FlextTestsProtocolsPayload.NativeMatchValue,
            /,
        ) -> bool: ...

    @runtime_checkable
    class ApproxLike(Protocol):
        """Structural stand-in for pytest approximation objects in type positions."""

        @property
        def expected(self) -> FlextTestsProtocolsPayload.NativeMatchValue: ...

        @property
        def rel(self) -> float | None: ...

        @property
        def abs(self) -> float | None: ...

        @property
        def nan_ok(self) -> bool: ...


__all__: list[str] = ["FlextTestsProtocolsMatchers"]
