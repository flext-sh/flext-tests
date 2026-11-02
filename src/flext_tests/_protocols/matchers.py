"""Callable contracts over native matcher values.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import t

from flext_tests._protocols import FlextTestsProtocolsPayload
from flext_tests._typings import FlextTestsTypesMatchers

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from typing import TypeAliasType

    from flext_cli import p


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

    @runtime_checkable
    class PayloadParams(Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class MatchRule[SubjectT = FlextTestsProtocolsPayload.NativeMatchValue](Protocol):
        """Structural data contract projected from the owning model."""

        eq: (
            FlextTestsProtocolsPayload.Payload
            | t.Port[FlextTestsProtocolsMatchers.ApproxLike]
            | t.Port[TypeAliasType]
            | None
        )
        ne: (
            FlextTestsProtocolsPayload.Payload
            | t.Port[FlextTestsProtocolsMatchers.ApproxLike]
            | t.Port[TypeAliasType]
            | None
        )
        is_: type | tuple[type, ...] | None
        has: FlextTestsProtocolsPayload.Payload | None
        lacks: FlextTestsProtocolsPayload.Payload | None
        none: bool | None
        empty: bool | None
        gt: FlextTestsTypesMatchers.ComparableScalar | None
        gte: FlextTestsTypesMatchers.ComparableScalar | None
        lt: FlextTestsTypesMatchers.ComparableScalar | None
        lte: FlextTestsTypesMatchers.ComparableScalar | None
        starts: str | None
        ends: str | None
        match: t.RegexPattern | None
        len: FlextTestsTypesMatchers.LengthSpec | None
        where: Callable[[SubjectT], bool] | None
        msg: str | None

    @runtime_checkable
    class FailParams(Protocol):
        """Structural data contract projected from the owning model."""

        msg: str | None
        has: FlextTestsTypesMatchers.ExclusionSpec | None
        lacks: FlextTestsTypesMatchers.ExclusionSpec | None
        starts: str | None
        ends: str | None
        match: t.RegexPattern | None
        code: str | None
        code_has: FlextTestsTypesMatchers.ErrorCodeSpec | None
        data: Mapping[str, FlextTestsProtocolsPayload.Payload] | None

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
        gt: FlextTestsTypesMatchers.ComparableScalar | None
        gte: FlextTestsTypesMatchers.ComparableScalar | None
        lt: FlextTestsTypesMatchers.ComparableScalar | None
        lte: FlextTestsTypesMatchers.ComparableScalar | None
        len: FlextTestsTypesMatchers.LengthSpec | None
        length_gt: int | None
        length_gte: int | None
        length_lt: int | None
        length_lte: int | None
        has: FlextTestsProtocolsPayload.Payload | None
        lacks: FlextTestsProtocolsPayload.Payload | None
        starts: str | None
        ends: str | None
        match: t.RegexPattern | None
        first: FlextTestsProtocolsPayload.Payload | None
        last: FlextTestsProtocolsPayload.Payload | None
        all_: (
            type | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool] | None
        )
        any_: (
            type | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool] | None
        )
        sorted: (
            bool
            | Callable[
                [FlextTestsProtocolsPayload.NativeMatchValue],
                FlextTestsProtocolsPayload.NativeMatchValue,
            ]
            | None
        )
        unique: bool | None
        keys: FlextTestsTypesMatchers.KeySpec | None
        lacks_keys: FlextTestsTypesMatchers.KeySpec | None
        values: Sequence[FlextTestsProtocolsPayload.Payload] | None
        kv: FlextTestsProtocolsPayload.Payload | None
        attrs: FlextTestsTypesMatchers.AttributeSpec | None
        methods: FlextTestsTypesMatchers.AttributeSpec | None
        attr_eq: FlextTestsProtocolsPayload.Payload | None
        ok: bool | None
        error: str | Sequence[str] | None
        deep: (
            Mapping[
                str,
                FlextTestsProtocolsPayload.Payload
                | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool],
            ]
            | None
        )
        paths: Mapping[str, FlextTestsProtocolsMatchers.MatchRule] | None
        items: (
            Sequence[FlextTestsProtocolsMatchers.MatchRule]
            | Mapping[str | int, FlextTestsProtocolsMatchers.MatchRule]
            | None
        )
        attrs_match: (
            Mapping[str, FlextTestsProtocolsMatchers.MatchRule[p.AttributeProbe]] | None
        )
        where: Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool] | None

    @runtime_checkable
    class ScopeParams(Protocol):
        """Structural data contract projected from the owning model."""

        settings: (
            Mapping[str, t.Port[FlextTestsProtocolsPayload.NativeMatchValue]] | None
        )
        container: (
            Mapping[str, t.Port[FlextTestsProtocolsPayload.NativeMatchValue]] | None
        )
        context: (
            Mapping[str, t.Port[FlextTestsProtocolsPayload.NativeMatchValue]] | None
        )
        cleanup: FlextTestsTypesMatchers.CleanupSpec | None
        env: FlextTestsTypesMatchers.EnvironmentSpec | None
        remove_env_keys: Sequence[str]
        python_paths: Sequence[str]
        cwd: Path | str | None

    @runtime_checkable
    class DeepMatchResult(Protocol):
        """Structural data contract projected from the owning model."""

        path: str
        expected: (
            FlextTestsProtocolsPayload.Payload
            | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool]
            | str
            | None
        )
        actual: FlextTestsProtocolsPayload.Payload | None
        matched: bool
        reason: str

    @runtime_checkable
    class Chain[TResult](Protocol):
        """Structural data contract projected from the owning model."""

        result: t.Port[p.Result[TResult]]

    @runtime_checkable
    class TestScope(Protocol):
        """Structural data contract projected from the owning model."""

        settings: Mapping[str, t.Port[FlextTestsProtocolsPayload.NativeMatchValue]]
        container: Mapping[str, t.Port[FlextTestsProtocolsPayload.NativeMatchValue]]
        context: Mapping[str, t.Port[FlextTestsProtocolsPayload.NativeMatchValue]]


__all__: list[str] = ["FlextTestsProtocolsMatchers"]
