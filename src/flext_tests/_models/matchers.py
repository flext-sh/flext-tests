"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import Annotated, ClassVar, Self, TypeAliasType

from flext_core import FlextModels, m, u
from flext_tests import p, t


class FlextTestsMatchersModelsMixin:
    class OkParams(FlextModels.Value):
        """Matcher parameters for successful result assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        eq: Annotated[
            (
                Mapping[str, t.Tests.TestobjectSerializable]
                | Sequence[t.Tests.TestobjectSerializable]
                | bytes
                | str
                | int
                | float
                | bool
                | TypeAliasType
                | None
            ),
            u.Field(
                description="Expected value (equality check)",
                union_mode="left_to_right",
            ),
        ] = None
        ne: Annotated[
            (
                Mapping[str, t.Tests.TestobjectSerializable]
                | Sequence[t.Tests.TestobjectSerializable]
                | bytes
                | str
                | int
                | float
                | bool
                | TypeAliasType
                | None
            ),
            u.Field(
                description="Value must not equal",
                union_mode="left_to_right",
            ),
        ] = None
        is_: Annotated[
            type | tuple[type, ...] | None,
            u.Field(
                validation_alias=t.AliasChoices("is_", "is"),
                description="Runtime type check",
            ),
        ] = None
        none: Annotated[bool | None, u.Field(description="None check")] = None
        empty: Annotated[bool | None, u.Field(description="Empty check")] = None
        gt: Annotated[float | int | None, u.Field(description="Greater than")] = None
        gte: Annotated[
            float | int | None, u.Field(description="Greater than or equal")
        ] = None
        lt: Annotated[float | int | None, u.Field(description="Less than")] = None
        lte: Annotated[
            float | int | None, u.Field(description="Less than or equal")
        ] = None
        has: Annotated[
            t.Tests.ContainmentSpec | None,
            u.Field(description="Unified containment check"),
        ] = None
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            u.Field(description="Unified non-containment check"),
        ] = None
        starts: Annotated[
            str | None, u.Field(description="String starts with prefix")
        ] = None
        ends: Annotated[str | None, u.Field(description="String ends with suffix")] = (
            None
        )
        match: Annotated[str | None, u.Field(description="Regex pattern")] = None
        len: Annotated[
            t.Tests.LengthSpec | None, u.Field(description="Length spec")
        ] = None
        deep: Annotated[
            t.Tests.DeepSpec | None, u.Field(description="Deep structural matching")
        ] = None
        path: Annotated[
            t.Tests.PathSpec | None,
            u.Field(
                description="Extract nested value via dot notation",
            ),
        ] = None
        paths: Annotated[
            t.Tests.PathMatchSpec | None,
            u.Field(description="Multiple path-based assertions"),
        ] = None
        items: Annotated[
            t.Tests.ItemMatchSpec | None,
            u.Field(description="Sequence item assertions by selector"),
        ] = None
        attrs_match: Annotated[
            t.Tests.AttributeMatchSpec | None,
            u.Field(description="Attribute assertions by attribute path"),
        ] = None
        where: Annotated[
            t.Tests.PredicateSpec | None,
            u.Field(description="Custom predicate function"),
        ] = None
        msg: Annotated[str | None, u.Field(description="Custom error message")] = None

    class FailParams(FlextModels.Value):
        """Matcher parameters for failure result assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        msg: Annotated[str | None, u.Field(description="Custom error message")] = None
        has: Annotated[
            t.Tests.ExclusionSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("has", "contains"),
                description="Error contains substring(s)",
            ),
        ] = None
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Error does NOT contain substring(s)",
            ),
        ] = None
        starts: Annotated[
            str | None, u.Field(description="Error starts with prefix")
        ] = None
        ends: Annotated[str | None, u.Field(description="Error ends with suffix")] = (
            None
        )
        match: Annotated[str | None, u.Field(description="Error matches regex")] = None
        code: Annotated[str | None, u.Field(description="Error code equals")] = None
        code_has: Annotated[
            t.Tests.ErrorCodeSpec | None,
            u.Field(description="Error code contains substring(s)"),
        ] = None
        data: Annotated[
            t.Tests.ErrorDataSpec | None,
            u.Field(description="Error data contains key-value pairs"),
        ] = None

    class ThatParams(FlextModels.Value):
        """Generic matcher parameters for value assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        msg: Annotated[str | None, u.Field(description="Custom error message")] = None
        eq: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Expected value (equality check)"),
        ] = None
        ne: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Value must not equal"),
        ] = None
        is_: Annotated[
            type | tuple[type, ...] | None,
            u.Field(
                validation_alias=t.AliasChoices("is_", "is"),
                description="Runtime type check",
            ),
        ] = None
        not_: Annotated[
            type | tuple[type, ...] | None,
            u.Field(
                validation_alias=t.AliasChoices("not_", "not"),
                description="Type check — value is NOT instance of type(s)",
            ),
        ] = None
        none: Annotated[bool | None, u.Field(description="None check")] = None
        empty: Annotated[bool | None, u.Field(description="Empty check")] = None
        gt: Annotated[float | int | None, u.Field(description="Greater than")] = None
        gte: Annotated[
            float | int | None, u.Field(description="Greater than or equal")
        ] = None
        lt: Annotated[float | int | None, u.Field(description="Less than")] = None
        lte: Annotated[
            float | int | None, u.Field(description="Less than or equal")
        ] = None
        len: Annotated[
            t.Tests.LengthSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("len", "length"),
                description="Length spec",
            ),
        ] = None
        length_gt: Annotated[int | None, u.Field(description="Length greater than")] = (
            None
        )
        length_gte: Annotated[
            int | None, u.Field(description="Length greater than or equal")
        ] = None
        length_lt: Annotated[int | None, u.Field(description="Length less than")] = None
        length_lte: Annotated[
            int | None, u.Field(description="Length less than or equal")
        ] = None
        has: Annotated[
            t.Tests.ContainmentSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("has", "contains"),
                description="Unified containment check",
            ),
        ] = None
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Unified non-containment check",
            ),
        ] = None
        starts: Annotated[
            str | None, u.Field(description="String starts with prefix")
        ] = None
        ends: Annotated[str | None, u.Field(description="String ends with suffix")] = (
            None
        )
        match: Annotated[str | None, u.Field(description="Regex pattern")] = None
        first: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Sequence first item equals"),
        ] = None
        last: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Sequence last item equals"),
        ] = None
        all_: Annotated[
            t.Tests.SequencePredicate | None,
            u.Field(
                validation_alias=t.AliasChoices("all_", "all"),
                description="All items match type or predicate",
            ),
        ] = None
        any_: Annotated[
            t.Tests.SequencePredicate | None,
            u.Field(
                validation_alias=t.AliasChoices("any_", "any"),
                description="Each item matches type or predicate",
            ),
        ] = None
        sorted: Annotated[t.Tests.SortKey | None, u.Field(description="Is sorted")] = (
            None
        )
        unique: Annotated[bool | None, u.Field(description="All items unique")] = None
        keys: Annotated[
            t.Tests.KeySpec | None, u.Field(description="Mapping has all keys")
        ] = None
        lacks_keys: Annotated[
            t.Tests.KeySpec | None, u.Field(description="Mapping missing keys")
        ] = None
        values: Annotated[
            Sequence[t.Tests.TestobjectSerializable] | None,
            u.Field(description="Mapping has all values"),
        ] = None
        kv: Annotated[
            t.Tests.KeyValueSpec | None, u.Field(description="Key-value pairs")
        ] = None
        attrs: Annotated[
            t.Tests.AttributeSpec | None, u.Field(description="Object has attribute(s)")
        ] = None
        methods: Annotated[
            t.Tests.AttributeSpec | None, u.Field(description="Object has method(s)")
        ] = None
        attr_eq: Annotated[
            t.Tests.AttributeValueSpec | None, u.Field(description="Attribute equals")
        ] = None
        ok: Annotated[bool | None, u.Field(description="For r: assert success")] = None
        error: Annotated[
            str | t.StrSequence | None, u.Field(description="For r: error contains")
        ] = None
        deep: Annotated[
            t.Tests.DeepSpec | None, u.Field(description="Deep structural matching")
        ] = None
        paths: Annotated[
            t.Tests.PathMatchSpec | None,
            u.Field(description="Multiple path-based assertions"),
        ] = None
        items: Annotated[
            t.Tests.ItemMatchSpec | None,
            u.Field(description="Sequence item assertions by selector"),
        ] = None
        attrs_match: Annotated[
            t.Tests.AttributeMatchSpec | None,
            u.Field(description="Attribute assertions by attribute path"),
        ] = None
        where: Annotated[
            t.Tests.PredicateSpec | None,
            u.Field(description="Custom predicate function"),
        ] = None

        @u.model_validator(mode="after")
        def normalize_legacy_parameters(self) -> Self:
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
                return self.model_copy(update=updates)
            return self

    class ScopeParams(FlextModels.Value):
        """Parameters for temporary test scope configuration."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        settings: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable] | None,
            u.Field(description="Initial configuration values"),
        ] = None
        container: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable] | None,
            u.Field(description="Initial container/service mappings"),
        ] = None
        context: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable] | None,
            u.Field(description="Initial context values"),
        ] = None
        cleanup: Annotated[
            t.Tests.CleanupSpec | None, u.Field(description="Cleanup functions")
        ] = None
        env: Annotated[
            t.Tests.EnvironmentSpec | None,
            u.Field(description="Temporary environment variables"),
        ] = None
        cwd: Annotated[
            Path | str | None, u.Field(description="Temporary working directory")
        ] = None

        @u.field_validator("cwd", mode="before")
        @classmethod
        def convert_cwd(cls, value: Path | str | None) -> Path | str | None:
            if isinstance(value, str):
                return Path(value)
            return value

    class DeepMatchResult(FlextModels.Value):
        """Structured output for deep-match comparisons."""

        path: Annotated[
            str,
            u.Field(description="Path where match occurred or failed"),
        ]
        expected: Annotated[
            t.Tests.TestobjectSerializable
            | Callable[[t.Tests.Testobject], bool]
            | None,
            u.Field(description="Expected value or predicate"),
        ]
        actual: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Actual value found"),
        ] = None
        matched: Annotated[bool, u.Field(description="Whether match succeeded")]
        reason: Annotated[str, u.Field(description="Reason for match failure")] = ""

    class Validate:
        """Centralized TypeAdapters for test data validation.

        All TypeAdapters used across flext_tests modules are defined here.
        Access via m.Tests.Validate.* with flat aliases.
        """

        DICT_ADAPTER: ClassVar[
            m.TypeAdapter[Mapping[str, t.Tests.TestobjectSerializable]]
        ] = t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER
        LIST_ADAPTER: ClassVar[
            m.TypeAdapter[Sequence[t.Tests.TestobjectSerializable]]
        ] = t.Tests.TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER

    class Chain[TResult](FlextModels.Value):
        """Container for chained result assertions."""

        result: Annotated[
            p.Result[TResult],
            u.Field(description="r being chained"),
        ]

    class TestScope(FlextModels.ArbitraryTypesModel):
        """Scope container for test configuration and runtime state."""

        __test__ = False

        settings: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable],
            u.Field(description="Configuration dictionary"),
        ] = u.Field(default_factory=dict)
        container: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable],
            u.Field(description="Container/service mappings"),
        ] = u.Field(default_factory=dict)
        context: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable],
            u.Field(description="Context values"),
        ] = u.Field(default_factory=dict)
