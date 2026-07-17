"""Structural contracts for matcher parameter and result models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable

    from flext_infra import p
    from flext_tests import t


class FlextTestsMatcherProtocolsMixin:
    """Read-only matcher contracts published under ``p.Tests``."""

    @runtime_checkable
    class OkParams(Protocol):
        """Parameters consumed by successful-result matchers."""

        @property
        def eq(self) -> t.Tests.MatcherEqTarget | None: ...

        @property
        def ne(self) -> t.Tests.MatcherEqTarget | None: ...

        @property
        def is_(
            self,
        ) -> type[p.AttributeProbe] | tuple[type[p.AttributeProbe], ...] | None: ...

        @property
        def none(self) -> bool | None: ...

        @property
        def empty(self) -> bool | None: ...

        @property
        def gt(self) -> t.Tests.ComparableScalar | None: ...

        @property
        def gte(self) -> t.Tests.ComparableScalar | None: ...

        @property
        def lt(self) -> t.Tests.ComparableScalar | None: ...

        @property
        def lte(self) -> t.Tests.ComparableScalar | None: ...

        @property
        def has(self) -> t.Tests.ContainmentSpec | None: ...

        @property
        def lacks(self) -> str | t.StrSequence | None: ...

        @property
        def starts(self) -> str | None: ...

        @property
        def ends(self) -> str | None: ...

        @property
        def match(self) -> t.RegexPattern | None: ...

        @property
        def len(self) -> t.Tests.LengthSpec | None: ...

        @property
        def deep(self) -> t.Tests.DeepSpec | None: ...

        @property
        def path(self) -> str | t.StrSequence | None: ...

        @property
        def paths(self) -> t.Tests.PathMatchSpec | None: ...

        @property
        def items(self) -> t.Tests.ItemMatchSpec | None: ...

        @property
        def attrs_match(self) -> t.Tests.AttributeMatchSpec | None: ...

        @property
        def where(self) -> t.Tests.PredicateSpec | None: ...

        @property
        def msg(self) -> str | None: ...

    @runtime_checkable
    class FailParams(Protocol):
        """Parameters consumed by failed-result matchers."""

        @property
        def msg(self) -> str | None: ...

        @property
        def has(self) -> str | t.StrSequence | None: ...

        @property
        def lacks(self) -> str | t.StrSequence | None: ...

        @property
        def starts(self) -> str | None: ...

        @property
        def ends(self) -> str | None: ...

        @property
        def match(self) -> t.RegexPattern | None: ...

        @property
        def code(self) -> str | None: ...

        @property
        def code_has(self) -> str | t.StrSequence | None: ...

        @property
        def data(self) -> t.JsonMapping | None: ...

    @runtime_checkable
    class ThatParams(Protocol):
        """Parameters consumed by generic value matchers."""

        @property
        def msg(self) -> str | None: ...

        @property
        def eq(self) -> t.Tests.TestobjectSerializable | None: ...

        @property
        def ne(self) -> t.Tests.TestobjectSerializable | None: ...

        @property
        def is_(
            self,
        ) -> type[p.AttributeProbe] | tuple[type[p.AttributeProbe], ...] | None: ...

        @property
        def not_(
            self,
        ) -> type[p.AttributeProbe] | tuple[type[p.AttributeProbe], ...] | None: ...

        @property
        def none(self) -> bool | None: ...

        @property
        def empty(self) -> bool | None: ...

        @property
        def gt(self) -> t.Tests.ComparableScalar | None: ...

        @property
        def gte(self) -> t.Tests.ComparableScalar | None: ...

        @property
        def lt(self) -> t.Tests.ComparableScalar | None: ...

        @property
        def lte(self) -> t.Tests.ComparableScalar | None: ...

        @property
        def len(self) -> t.Tests.LengthSpec | None: ...

        @property
        def has(self) -> t.Tests.ContainmentSpec | None: ...

        @property
        def lacks(self) -> str | t.StrSequence | None: ...

        @property
        def starts(self) -> str | None: ...

        @property
        def ends(self) -> str | None: ...

        @property
        def match(self) -> t.RegexPattern | None: ...

        @property
        def first(self) -> t.Tests.TestobjectSerializable | None: ...

        @property
        def last(self) -> t.Tests.TestobjectSerializable | None: ...

        @property
        def all_(self) -> t.Tests.SequencePredicate | None: ...

        @property
        def any_(self) -> t.Tests.SequencePredicate | None: ...

        @property
        def sorted(self) -> t.Tests.SortKey | None: ...

        @property
        def unique(self) -> bool | None: ...

        @property
        def keys(self) -> t.Tests.KeySpec | None: ...

        @property
        def lacks_keys(self) -> t.Tests.KeySpec | None: ...

        @property
        def values(self) -> t.SequenceOf[t.Tests.TestobjectSerializable] | None: ...

        @property
        def kv(self) -> t.Tests.KeyValueSpec | None: ...

        @property
        def attrs(self) -> str | t.StrSequence | None: ...

        @property
        def methods(self) -> str | t.StrSequence | None: ...

        @property
        def attr_eq(self) -> t.Tests.AttributeValueSpec | None: ...

        @property
        def ok(self) -> bool | None: ...

        @property
        def deep(self) -> t.Tests.DeepSpec | None: ...

        @property
        def paths(self) -> t.Tests.PathMatchSpec | None: ...

        @property
        def items(self) -> t.Tests.ItemMatchSpec | None: ...

        @property
        def attrs_match(self) -> t.Tests.AttributeMatchSpec | None: ...

        @property
        def where(self) -> t.Tests.PredicateSpec | None: ...

    @runtime_checkable
    class DeepMatchResult(Protocol):
        """Outcome of one recursive structural comparison."""

        @property
        def path(self) -> str: ...

        @property
        def expected(
            self,
        ) -> (
            t.Tests.TestobjectSerializable
            | Callable[[t.Tests.TestobjectSerializable], bool]
            | None
        ): ...

        @property
        def actual(self) -> t.Tests.TestobjectSerializable | None: ...

        @property
        def matched(self) -> bool: ...

        @property
        def reason(self) -> str: ...

    @runtime_checkable
    class Chain[ResultT](Protocol):
        """Chained result matcher state."""

        @property
        def result(self) -> p.Result[ResultT]: ...

    @runtime_checkable
    class TestScope(Protocol):
        """Temporary matcher scope state."""

        @property
        def settings(self) -> t.MappingKV[str, t.Tests.TestobjectSerializable]: ...

        @property
        def container(self) -> t.MappingKV[str, t.Tests.TestobjectSerializable]: ...

        @property
        def context(self) -> t.MappingKV[str, t.Tests.TestobjectSerializable]: ...


__all__: tuple[str, ...] = ("FlextTestsMatcherProtocolsMixin",)
