"""Callable contracts over native matcher values.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping, Sequence
from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols, t

from flext_tests._protocols import FlextTestsProtocolsPayload
from flext_tests._typings import FlextTestsTypesMatchers

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from typing import TypeAliasType

    from flext_cli import p

    from flext_tests._protocols import FlextTestsProtocolsBase


@runtime_checkable
class FlextTestsProtocolsMatchers(Protocol):
    """Structural matcher capabilities without recursive type aliases."""

    type MatcherOption = (
        FlextTestsProtocolsPayload.NativeMatchValue
        | FlextTestsProtocolsBase.Payload
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
            | FlextTestsProtocolsBase.Payload
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
    class PayloadParams(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class MatchRule[SubjectT = FlextTestsProtocolsPayload.NativeMatchValue](
        PayloadParams, Protocol
    ):
        """Structural data contract projected from the owning model."""

        @property
        def eq(
            self,
        ) -> (
            FlextTestsProtocolsBase.Payload
            | t.Port[FlextTestsProtocolsMatchers.ApproxLike]
            | t.Port[TypeAliasType]
            | None
        ):
            """Expected equality value."""
            ...

        @property
        def ne(
            self,
        ) -> (
            FlextTestsProtocolsBase.Payload
            | t.Port[FlextTestsProtocolsMatchers.ApproxLike]
            | t.Port[TypeAliasType]
            | None
        ):
            """Expected inequality value."""
            ...

        @property
        def is_(self) -> type | tuple[type, ...] | None:
            """Expected runtime type."""
            ...

        @property
        def has(self) -> FlextTestsProtocolsBase.Payload | None:
            """Required contained value."""
            ...

        @property
        def lacks(self) -> FlextTestsProtocolsBase.Payload | None:
            """Forbidden contained value."""
            ...

        @property
        def none(self) -> bool | None:
            """Expected null state."""
            ...

        @property
        def empty(self) -> bool | None:
            """Expected empty state."""
            ...

        @property
        def gt(self) -> FlextTestsTypesMatchers.ComparableScalar | None:
            """Exclusive lower bound."""
            ...

        @property
        def gte(self) -> FlextTestsTypesMatchers.ComparableScalar | None:
            """Inclusive lower bound."""
            ...

        @property
        def lt(self) -> FlextTestsTypesMatchers.ComparableScalar | None:
            """Exclusive upper bound."""
            ...

        @property
        def lte(self) -> FlextTestsTypesMatchers.ComparableScalar | None:
            """Inclusive upper bound."""
            ...

        @property
        def starts(self) -> str | None:
            """Required string prefix."""
            ...

        @property
        def ends(self) -> str | None:
            """Required string suffix."""
            ...

        @property
        def match(self) -> t.RegexPattern | None:
            """Required regular expression."""
            ...

        @property
        def len(self) -> FlextTestsTypesMatchers.LengthSpec | None:
            """Required length."""
            ...

        @property
        def where(self) -> Callable[[SubjectT], bool] | None:
            """Predicate applied to the subject."""
            ...

        @property
        def msg(self) -> str | None:
            """Inherited assertion message."""
            ...

    @runtime_checkable
    class FailParams(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def msg(self) -> str | None:
            """Custom error message."""
            ...

        @property
        def has(self) -> FlextTestsTypesMatchers.ExclusionSpec | None:
            """Error contains substrings."""
            ...

        @property
        def lacks(self) -> FlextTestsTypesMatchers.ExclusionSpec | None:
            """Error does not contain substrings."""
            ...

        @property
        def starts(self) -> str | None:
            """Error starts with prefix."""
            ...

        @property
        def ends(self) -> str | None:
            """Error ends with suffix."""
            ...

        @property
        def match(self) -> t.RegexPattern | None:
            """Error matches compiled regex."""
            ...

        @property
        def code(self) -> str | None:
            """Error code equals."""
            ...

        @property
        def code_has(self) -> FlextTestsTypesMatchers.ErrorCodeSpec | None:
            """Error code contains substrings."""
            ...

        @property
        def data(self) -> Mapping[str, FlextTestsProtocolsBase.Payload] | None:
            """Error data contains key-value pairs."""
            ...

    @runtime_checkable
    class ThatParams(PayloadParams, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def msg(self) -> str | None:
            """Message."""
            ...

        @property
        def truth(self) -> bool | None:
            """Native truth value of the original subject."""
            ...

        @property
        def assertion_message(self) -> p.AttributeProbe | None:
            """Original assertion message, passed inside its failure branch."""
            ...

        @property
        def is_(self) -> type | tuple[type, ...] | None:
            """Type."""
            ...

        @property
        def not_(self) -> type | tuple[type, ...] | None:
            """Not type."""
            ...

        @property
        def none(self) -> bool | None:
            """None check."""
            ...

        @property
        def empty(self) -> bool | None:
            """Empty check."""
            ...

        @property
        def gt(self) -> FlextTestsTypesMatchers.ComparableScalar | None:
            """Greater than."""
            ...

        @property
        def gte(self) -> FlextTestsTypesMatchers.ComparableScalar | None:
            """Greater/equal."""
            ...

        @property
        def lt(self) -> FlextTestsTypesMatchers.ComparableScalar | None:
            """Less than."""
            ...

        @property
        def lte(self) -> FlextTestsTypesMatchers.ComparableScalar | None:
            """Less/equal."""
            ...

        @property
        def len(self) -> FlextTestsTypesMatchers.LengthSpec | None:
            """Length."""
            ...

        @property
        def length_gt(self) -> int | None:
            """Length >."""
            ...

        @property
        def length_gte(self) -> int | None:
            """Length >=."""
            ...

        @property
        def length_lt(self) -> int | None:
            """Length <."""
            ...

        @property
        def length_lte(self) -> int | None:
            """Length <=."""
            ...

        @property
        def has(self) -> FlextTestsProtocolsBase.Payload | None:
            """Contains."""
            ...

        @property
        def lacks(self) -> FlextTestsProtocolsBase.Payload | None:
            """Lacks."""
            ...

        @property
        def starts(self) -> str | None:
            """Prefix."""
            ...

        @property
        def ends(self) -> str | None:
            """Suffix."""
            ...

        @property
        def match(self) -> t.RegexPattern | None:
            """Regex."""
            ...

        @property
        def first(self) -> FlextTestsProtocolsBase.Payload | None:
            """First item."""
            ...

        @property
        def last(self) -> FlextTestsProtocolsBase.Payload | None:
            """Last item."""
            ...

        @property
        def all_(
            self,
        ) -> (
            type | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool] | None
        ):
            """All."""
            ...

        @property
        def any_(
            self,
        ) -> (
            type | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool] | None
        ):
            """Any."""
            ...

        @property
        def sorted(
            self,
        ) -> (
            bool
            | Callable[
                [FlextTestsProtocolsPayload.NativeMatchValue],
                FlextTestsProtocolsPayload.NativeMatchValue,
            ]
            | None
        ):
            """Sort key."""
            ...

        @property
        def unique(self) -> bool | None:
            """Unique."""
            ...

        @property
        def keys(self) -> FlextTestsTypesMatchers.KeySpec | None:
            """Keys."""
            ...

        @property
        def lacks_keys(self) -> FlextTestsTypesMatchers.KeySpec | None:
            """No keys."""
            ...

        @property
        def values(self) -> Sequence[FlextTestsProtocolsBase.Payload] | None:
            """Values."""
            ...

        @property
        def kv(self) -> FlextTestsProtocolsBase.Payload | None:
            """Key-values."""
            ...

        @property
        def attrs(self) -> FlextTestsTypesMatchers.AttributeSpec | None:
            """Attrs."""
            ...

        @property
        def methods(self) -> FlextTestsTypesMatchers.AttributeSpec | None:
            """Methods."""
            ...

        @property
        def attr_eq(self) -> FlextTestsProtocolsBase.Payload | None:
            """Attr equals."""
            ...

        @property
        def ok(self) -> bool | None:
            """Result ok."""
            ...

        @property
        def error(self) -> str | Sequence[str] | None:
            """Result error."""
            ...

        @property
        def deep(
            self,
        ) -> (
            Mapping[
                str,
                FlextTestsProtocolsBase.Payload
                | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool],
            ]
            | None
        ):
            """Deep spec."""
            ...

        @property
        def paths(self) -> Mapping[str, FlextTestsProtocolsMatchers.MatchRule] | None:
            """Paths."""
            ...

        @property
        def items(
            self,
        ) -> (
            Sequence[FlextTestsProtocolsMatchers.MatchRule]
            | Mapping[str | int, FlextTestsProtocolsMatchers.MatchRule]
            | None
        ):
            """Items."""
            ...

        @property
        def attrs_match(
            self,
        ) -> (
            Mapping[str, FlextTestsProtocolsMatchers.MatchRule[p.AttributeProbe]] | None
        ):
            """Attr rules."""
            ...

        @property
        def where(
            self,
        ) -> Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool] | None:
            """Predicate."""
            ...

    @runtime_checkable
    class ScopeParams(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def settings(
            self,
        ) -> Mapping[str, FlextTestsProtocolsPayload.NativeMatchValue] | None:
            """Initial configuration values."""
            ...

        @property
        def container(
            self,
        ) -> Mapping[str, FlextTestsProtocolsPayload.NativeMatchValue] | None:
            """Initial container/service mappings."""
            ...

        @property
        def context(
            self,
        ) -> Mapping[str, FlextTestsProtocolsPayload.NativeMatchValue] | None:
            """Initial context values."""
            ...

        @property
        def cleanup(self) -> FlextTestsTypesMatchers.CleanupSpec | None:
            """Cleanup functions."""
            ...

        @property
        def env(self) -> FlextTestsTypesMatchers.EnvironmentSpec | None:
            """Temporary environment variables."""
            ...

        @property
        def remove_env_keys(self) -> Sequence[str]:
            """Environment variables absent inside the scope."""
            ...

        @property
        def python_paths(self) -> Sequence[str]:
            """Import roots prepended inside the scope."""
            ...

        @property
        def cwd(self) -> Path | str | None:
            """Temporary working directory."""
            ...

    @runtime_checkable
    class DeepMatchResult(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def path(self) -> str:
            """Path where matching occurred."""
            ...

        @property
        def expected(
            self,
        ) -> (
            FlextTestsProtocolsBase.Payload
            | Callable[[FlextTestsProtocolsPayload.NativeMatchValue], bool]
            | str
            | None
        ):
            """Expected value or predicate."""
            ...

        @property
        def actual(self) -> FlextTestsProtocolsBase.Payload | None:
            """Actual value found."""
            ...

        @property
        def matched(self) -> bool:
            """Whether match succeeded."""
            ...

        @property
        def reason(self) -> str:
            """Reason for match failure."""
            ...

    @runtime_checkable
    class Chain[TResult](FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def result(self) -> p.Result[TResult]:
            """Result being chained."""
            ...

    @runtime_checkable
    class TestScope(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def settings(self) -> Mapping[str, FlextTestsProtocolsPayload.NativeMatchValue]:
            """Configuration dictionary."""
            ...

        @property
        def container(
            self,
        ) -> Mapping[str, FlextTestsProtocolsPayload.NativeMatchValue]:
            """Container/service mappings."""
            ...

        @property
        def context(self) -> Mapping[str, FlextTestsProtocolsPayload.NativeMatchValue]:
            """Context values."""
            ...


__all__: list[str] = ["FlextTestsProtocolsMatchers"]
