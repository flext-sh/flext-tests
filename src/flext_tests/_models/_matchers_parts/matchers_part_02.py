"""Generic matcher parameter models for flext-tests."""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Annotated, ClassVar

from flext_infra.models import m
from flext_infra.utilities import u
from flext_tests import t
from flext_tests._models._matchers_parts.matchers_part_01 import (
    FlextTestsMatchersModelsMixin as FlextTestsMatchersModelsMixinPart01,
)

if TYPE_CHECKING:
    from collections.abc import MutableMapping


class FlextTestsMatchersModelsMixin(FlextTestsMatchersModelsMixinPart01):
    """Generic matcher parameter models for flext-tests."""

    class ThatParams(m.Value):
        """Generic matcher parameters for value assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
        )

        msg: Annotated[str | None, u.Field(description="Message.")] = None
        eq: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Equals."),
        ] = None
        ne: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Not equals."),
        ] = None
        is_: Annotated[
            type[object] | tuple[type[object], ...] | None,
            u.Field(validation_alias=t.AliasChoices("is_", "is"), description="Type."),
        ] = None
        not_: Annotated[
            type[object] | tuple[type[object], ...] | None,
            u.Field(
                validation_alias=t.AliasChoices("not_", "not"),
                description="Not type.",
            ),
        ] = None
        none: Annotated[bool | None, u.Field(description="None check.")] = None
        empty: Annotated[bool | None, u.Field(description="Empty check.")] = None
        gt: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Greater than."),
        ] = None
        gte: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Greater/equal."),
        ] = None
        lt: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Less than."),
        ] = None
        lte: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Less/equal."),
        ] = None
        len: Annotated[
            t.Tests.LengthSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("len", "length"),
                description="Length.",
            ),
        ] = None
        length_gt: Annotated[int | None, u.Field(description="Length >.")] = None
        length_gte: Annotated[int | None, u.Field(description="Length >=.")] = None
        length_lt: Annotated[int | None, u.Field(description="Length <.")] = None
        length_lte: Annotated[int | None, u.Field(description="Length <=.")] = None
        has: Annotated[
            t.Tests.ContainmentSpec | None,
            m.SkipValidation,
            u.Field(
                validation_alias=t.AliasChoices("has", "contains"),
                description="Contains.",
            ),
        ] = None
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Lacks.",
            ),
        ] = None
        starts: Annotated[str | None, u.Field(description="Prefix.")] = None
        ends: Annotated[str | None, u.Field(description="Suffix.")] = None
        match: Annotated[t.Infra.RegexPattern | None, u.Field(description="Regex.")] = (
            None
        )
        first: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="First item."),
        ] = None
        last: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Last item."),
        ] = None
        all_: Annotated[
            t.Tests.SequencePredicate | None,
            m.SkipValidation,
            u.Field(validation_alias=t.AliasChoices("all_", "all"), description="All."),
        ] = None
        any_: Annotated[
            t.Tests.SequencePredicate | None,
            m.SkipValidation,
            u.Field(validation_alias=t.AliasChoices("any_", "any"), description="Any."),
        ] = None
        sorted: Annotated[t.Tests.SortKey | None, u.Field(description="Sort key.")] = (
            None
        )
        unique: Annotated[bool | None, u.Field(description="Unique.")] = None
        keys: Annotated[t.Tests.KeySpec | None, u.Field(description="Keys.")] = None
        lacks_keys: Annotated[
            t.Tests.KeySpec | None,
            u.Field(description="No keys."),
        ] = None
        values: Annotated[
            t.SequenceOf[t.Tests.TestobjectSerializable] | None,
            u.Field(description="Values."),
        ] = None
        kv: Annotated[
            t.Tests.KeyValueSpec | None,
            u.Field(description="Key-values."),
        ] = None
        attrs: Annotated[
            t.Tests.AttributeSpec | None,
            u.Field(description="Attrs."),
        ] = None
        methods: Annotated[
            t.Tests.AttributeSpec | None,
            u.Field(description="Methods."),
        ] = None
        attr_eq: Annotated[
            t.Tests.AttributeValueSpec | None,
            u.Field(description="Attr equals."),
        ] = None
        ok: Annotated[bool | None, u.Field(description="Result ok.")] = None
        error: Annotated[
            str | t.StrSequence | None,
            u.Field(description="Result error."),
        ] = None
        deep: Annotated[t.Tests.DeepSpec | None, u.Field(description="Deep spec.")] = (
            None
        )
        paths: Annotated[
            t.Tests.PathMatchSpec | None,
            m.SkipValidation,
            u.Field(description="Paths."),
        ] = None
        items: Annotated[
            t.Tests.ItemMatchSpec | None,
            m.SkipValidation,
            u.Field(description="Items."),
        ] = None
        attrs_match: Annotated[
            t.Tests.AttributeMatchSpec | None,
            m.SkipValidation,
            u.Field(description="Attr rules."),
        ] = None
        where: Annotated[
            t.Tests.PredicateSpec | None,
            m.SkipValidation,
            u.Field(description="Predicate."),
        ] = None

        @u.model_validator(mode="after")
        def normalize_legacy_parameters(
            self,
        ) -> FlextTestsMatchersModelsMixin.ThatParams:
            """Normalize legacy aliases into canonical matcher fields."""
            updates: MutableMapping[str, t.Tests.TestobjectSerializable] = {}
            if self.error is not None and self.has is None:
                updates["has"] = self.error
            if self.len is None and any(
                v is not None
                for v in (
                    self.length_gt,
                    self.length_gte,
                    self.length_lt,
                    self.length_lte,
                )
            ):
                min_len = 0
                max_len = sys.maxsize
                if self.length_gt is not None:
                    min_len = self.length_gt + 1
                if self.length_gte is not None:
                    min_len = max(min_len, self.length_gte)
                if self.length_lt is not None:
                    max_len = self.length_lt - 1
                if self.length_lte is not None:
                    max_len = min(max_len, self.length_lte)
                updates["len"] = (min_len, max_len)
            if updates:
                payload = self.model_dump()
                payload.update(updates)
                return FlextTestsMatchersModelsMixin.ThatParams(**payload)
            return self


__all__: list[str] = ["FlextTestsMatchersModelsMixin"]
