"""Callable contracts over native matcher values.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_tests import p, t

if TYPE_CHECKING:
    from collections.abc import Callable

    from flext_tests._protocols import FlextTestsProtocolsPayload


@runtime_checkable
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
        | t.Tests.LengthSpec
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

    @runtime_checkable
    class PayloadParams(Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class MatchRule(Protocol):
        """Structural data contract projected from the owning model."""

        eq: p.Tests.Payload | t.Port[p.Tests.ApproxLike] | t.Port[TypeAliasType] | None
        ne: p.Tests.Payload | t.Port[p.Tests.ApproxLike] | t.Port[TypeAliasType] | None
        is_: type | tuple[type, ...] | None
        has: p.Tests.Payload | None
        lacks: p.Tests.Payload | None
        none: bool | None
        empty: bool | None
        gt: t.Tests.ComparableScalar | None
        gte: t.Tests.ComparableScalar | None
        lt: t.Tests.ComparableScalar | None
        lte: t.Tests.ComparableScalar | None
        starts: str | None
        ends: str | None
        match: t.RegexPattern | None
        len: t.Tests.LengthSpec | None
        where: Callable[[SubjectT], bool] | None
        msg: str | None

    @runtime_checkable
    class FailParams(Protocol):
        """Structural data contract projected from the owning model."""

        msg: str | None
        has: t.Tests.ExclusionSpec | None
        lacks: t.Tests.ExclusionSpec | None
        starts: str | None
        ends: str | None
        match: t.RegexPattern | None
        code: str | None
        code_has: t.Tests.ErrorCodeSpec | None
        data: Mapping[str, p.Tests.Payload] | None

    @runtime_checkable
    class ThatParams(Protocol):
        """Structural data contract projected from the owning model."""

        msg: str | None
        truth: bool | None
        assertion_message: t.Port[p.AttributeProbe] | None
        is_: type | tuple[type, ...] | None
        not_: type | tuple[type, ...] | None
        none: bool | None
        empty: bool | None
        gt: t.Tests.ComparableScalar | None
        gte: t.Tests.ComparableScalar | None
        lt: t.Tests.ComparableScalar | None
        lte: t.Tests.ComparableScalar | None
        len: t.Tests.LengthSpec | None
        length_gt: int | None
        length_gte: int | None
        length_lt: int | None
        length_lte: int | None
        has: p.Tests.Payload | None
        lacks: p.Tests.Payload | None
        starts: str | None
        ends: str | None
        match: t.RegexPattern | None
        first: p.Tests.Payload | None
        last: p.Tests.Payload | None
        all_: type | Callable[[p.Tests.NativeMatchValue], bool] | None
        any_: type | Callable[[p.Tests.NativeMatchValue], bool] | None
        sorted: (
            bool | Callable[[p.Tests.NativeMatchValue], p.Tests.NativeMatchValue] | None
        )
        unique: bool | None
        keys: t.Tests.KeySpec | None
        lacks_keys: t.Tests.KeySpec | None
        values: Sequence[p.Tests.Payload] | None
        kv: p.Tests.Payload | None
        attrs: t.Tests.AttributeSpec | None
        methods: t.Tests.AttributeSpec | None
        attr_eq: p.Tests.Payload | None
        ok: bool | None
        error: str | Sequence[str] | None
        deep: (
            Mapping[str, p.Tests.Payload | Callable[[p.Tests.NativeMatchValue], bool]]
            | None
        )
        paths: Mapping[str, p.Tests.MatchRule] | None
        items: (
            Sequence[p.Tests.MatchRule] | Mapping[str | int, p.Tests.MatchRule] | None
        )
        attrs_match: Mapping[str, p.Tests.MatchRule[p.AttributeProbe]] | None
        where: Callable[[p.Tests.NativeMatchValue], bool] | None

    @runtime_checkable
    class ScopeParams(Protocol):
        """Structural data contract projected from the owning model."""

        settings: Mapping[str, t.Port[p.Tests.NativeMatchValue]] | None
        container: Mapping[str, t.Port[p.Tests.NativeMatchValue]] | None
        context: Mapping[str, t.Port[p.Tests.NativeMatchValue]] | None
        cleanup: t.Tests.CleanupSpec | None
        env: t.Tests.EnvironmentSpec | None
        remove_env_keys: Sequence[str]
        python_paths: Sequence[str]
        cwd: Path | str | None

    @runtime_checkable
    class DeepMatchResult(Protocol):
        """Structural data contract projected from the owning model."""

        path: str
        expected: (
            p.Tests.Payload | Callable[[p.Tests.NativeMatchValue], bool] | str | None
        )
        actual: p.Tests.Payload | None
        matched: bool
        reason: str

    @runtime_checkable
    class Chain(Protocol):
        """Structural data contract projected from the owning model."""

        result: t.Port[p.Result[TResult]]

    @runtime_checkable
    class TestScope(Protocol):
        """Structural data contract projected from the owning model."""

        settings: Mapping[str, t.Port[p.Tests.NativeMatchValue]]
        container: Mapping[str, t.Port[p.Tests.NativeMatchValue]]
        context: Mapping[str, t.Port[p.Tests.NativeMatchValue]]


__all__: list[str] = ["FlextTestsProtocolsMatchers"]
