"""Callable contracts over native matcher values.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from flext_tests import t
    from flext_tests._protocols.payload import FlextTestsPayloadProtocolsMixin


class FlextTestsMatchersProtocolsMixin(Protocol):
    """Structural matcher capabilities without recursive type aliases."""

    @runtime_checkable
    class MatcherCriteriaMapping(Protocol):
        """Read nested native matcher criteria independently of payload values."""

        def __len__(self) -> int:
            """Return the number of declared criteria."""
            ...

        def items(
            self,
        ) -> Iterable[tuple[str | int, t.Tests.MatcherOption]]:
            """Iterate selectors and their unchanged native criteria."""
            ...

    @runtime_checkable
    class MatcherCriteriaSequence(Protocol):
        """Read ordered native criteria without converting their operands."""

        def __len__(self) -> int:
            """Return the number of positional criteria."""
            ...

        def __iter__(self) -> Iterator[t.Tests.MatcherOption]:
            """Iterate the original criteria."""
            ...

        def __getitem__(self, index: int, /) -> t.Tests.MatcherOption:
            """Read one positional criterion."""
            ...

    @runtime_checkable
    class MatchPredicate(Protocol):
        """Evaluate the native value a matcher criterion is applied to."""

        def __call__(
            self,
            value: FlextTestsPayloadProtocolsMixin.NativeMatchValue,
            /,
        ) -> bool: ...

    @runtime_checkable
    class ApproxLike(Protocol):
        """Structural stand-in for pytest approximation objects in type positions."""

        @property
        def expected(self) -> FlextTestsPayloadProtocolsMixin.NativeMatchValue: ...

        @property
        def rel(self) -> float | None: ...

        @property
        def abs(self) -> float | None: ...

        @property
        def nan_ok(self) -> bool: ...


__all__: list[str] = ["FlextTestsMatchersProtocolsMixin"]
