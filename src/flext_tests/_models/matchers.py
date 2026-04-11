"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping, MutableMapping, Sequence
from pathlib import Path
from typing import Annotated, ClassVar, Self, TypeAliasType

from pydantic import (
    AliasChoices,
    ConfigDict,
    Field,
    TypeAdapter,
    field_validator,
    model_validator,
)

from flext_core import FlextModels, r
from flext_tests import p, t


class FlextTestsMatchersModelsMixin:
    class OkParams(FlextModels.Value):
        """Matcher parameters for successful result assertions."""

        model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

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
            Field(
                default=None,
                description="Expected value (equality check)",
                union_mode="left_to_right",
            ),
        ]
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
            Field(
                default=None,
                description="Value must not equal",
                union_mode="left_to_right",
            ),
        ]
        is_: Annotated[
            type | tuple[type, ...] | None,
            Field(
                default=None,
                validation_alias=AliasChoices("is_", "is"),
                description="Runtime type check",
            ),
        ]
        none: Annotated[bool | None, Field(default=None, description="None check")]
        empty: Annotated[
            bool | None,
            Field(default=None, description="Empty check"),
        ]
        gt: Annotated[
            float | int | None,
            Field(default=None, description="Greater than"),
        ]
        gte: Annotated[
            float | int | None,
            Field(default=None, description="Greater than or equal"),
        ]
        lt: Annotated[
            float | int | None,
            Field(default=None, description="Less than"),
        ]
        lte: Annotated[
            float | int | None,
            Field(default=None, description="Less than or equal"),
        ]
        has: Annotated[
            t.Tests.ContainmentSpec | None,
            Field(default=None, description="Unified containment check"),
        ]
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            Field(default=None, description="Unified non-containment check"),
        ]
        starts: Annotated[
            str | None,
            Field(default=None, description="String starts with prefix"),
        ]
        ends: Annotated[
            str | None,
            Field(default=None, description="String ends with suffix"),
        ]
        match: Annotated[
            str | None,
            Field(default=None, description="Regex pattern"),
        ]
        len: Annotated[
            t.Tests.LengthSpec | None,
            Field(default=None, description="Length spec"),
        ]
        deep: Annotated[
            t.Tests.DeepSpec | None,
            Field(default=None, description="Deep structural matching"),
        ]
        path: Annotated[
            t.Tests.PathSpec | None,
            Field(
                default=None,
                description="Extract nested value via dot notation",
            ),
        ]
        where: Annotated[
            t.Tests.PredicateSpec | None,
            Field(default=None, description="Custom predicate function"),
        ]
        msg: Annotated[
            str | None,
            Field(default=None, description="Custom error message"),
        ]

    class FailParams(FlextModels.Value):
        """Matcher parameters for failure result assertions."""

        model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

        msg: Annotated[
            str | None,
            Field(default=None, description="Custom error message"),
        ]
        has: Annotated[
            t.Tests.ExclusionSpec | None,
            Field(
                default=None,
                validation_alias=AliasChoices("has", "contains"),
                description="Error contains substring(s)",
            ),
        ]
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            Field(
                default=None,
                validation_alias=AliasChoices("lacks", "excludes"),
                description="Error does NOT contain substring(s)",
            ),
        ]
        starts: Annotated[
            str | None,
            Field(default=None, description="Error starts with prefix"),
        ]
        ends: Annotated[
            str | None,
            Field(default=None, description="Error ends with suffix"),
        ]
        match: Annotated[
            str | None,
            Field(default=None, description="Error matches regex"),
        ]
        code: Annotated[
            str | None,
            Field(default=None, description="Error code equals"),
        ]
        code_has: Annotated[
            t.Tests.ErrorCodeSpec | None,
            Field(default=None, description="Error code contains substring(s)"),
        ]
        data: Annotated[
            t.Tests.ErrorDataSpec | None,
            Field(default=None, description="Error data contains key-value pairs"),
        ]

    class ThatParams(FlextModels.Value):
        """Generic matcher parameters for value assertions."""

        model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

        msg: Annotated[
            str | None,
            Field(default=None, description="Custom error message"),
        ]
        eq: Annotated[
            t.Tests.TestobjectSerializable | None,
            Field(default=None, description="Expected value (equality check)"),
        ]
        ne: Annotated[
            t.Tests.TestobjectSerializable | None,
            Field(default=None, description="Value must not equal"),
        ]
        is_: Annotated[
            type | tuple[type, ...] | None,
            Field(
                default=None,
                validation_alias=AliasChoices("is_", "is"),
                description="Runtime type check",
            ),
        ]
        not_: Annotated[
            type | tuple[type, ...] | None,
            Field(
                default=None,
                validation_alias=AliasChoices("not_", "not"),
                description="Type check — value is NOT instance of type(s)",
            ),
        ]
        none: Annotated[bool | None, Field(default=None, description="None check")]
        empty: Annotated[
            bool | None,
            Field(default=None, description="Empty check"),
        ]
        gt: Annotated[
            float | int | None,
            Field(default=None, description="Greater than"),
        ]
        gte: Annotated[
            float | int | None,
            Field(default=None, description="Greater than or equal"),
        ]
        lt: Annotated[
            float | int | None,
            Field(default=None, description="Less than"),
        ]
        lte: Annotated[
            float | int | None,
            Field(default=None, description="Less than or equal"),
        ]
        len: Annotated[
            t.Tests.LengthSpec | None,
            Field(
                default=None,
                validation_alias=AliasChoices("len", "length"),
                description="Length spec",
            ),
        ]
        length_gt: Annotated[
            int | None,
            Field(default=None, description="Length greater than"),
        ]
        length_gte: Annotated[
            int | None,
            Field(default=None, description="Length greater than or equal"),
        ]
        length_lt: Annotated[
            int | None,
            Field(default=None, description="Length less than"),
        ]
        length_lte: Annotated[
            int | None,
            Field(default=None, description="Length less than or equal"),
        ]
        has: Annotated[
            t.Tests.ContainmentSpec | None,
            Field(
                default=None,
                validation_alias=AliasChoices("has", "contains"),
                description="Unified containment check",
            ),
        ]
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            Field(
                default=None,
                validation_alias=AliasChoices("lacks", "excludes"),
                description="Unified non-containment check",
            ),
        ]
        starts: Annotated[
            str | None,
            Field(default=None, description="String starts with prefix"),
        ]
        ends: Annotated[
            str | None,
            Field(default=None, description="String ends with suffix"),
        ]
        match: Annotated[
            str | None,
            Field(default=None, description="Regex pattern"),
        ]
        first: Annotated[
            t.Tests.TestobjectSerializable | None,
            Field(default=None, description="Sequence first item equals"),
        ]
        last: Annotated[
            t.Tests.TestobjectSerializable | None,
            Field(default=None, description="Sequence last item equals"),
        ]
        all_: Annotated[
            t.Tests.SequencePredicate | None,
            Field(
                default=None,
                validation_alias=AliasChoices("all_", "all"),
                description="All items match type or predicate",
            ),
        ]
        any_: Annotated[
            t.Tests.SequencePredicate | None,
            Field(
                default=None,
                validation_alias=AliasChoices("any_", "any"),
                description="Each item matches type or predicate",
            ),
        ]
        sorted: Annotated[
            t.Tests.SortKey | None,
            Field(default=None, description="Is sorted"),
        ]
        unique: Annotated[
            bool | None,
            Field(default=None, description="All items unique"),
        ]
        keys: Annotated[
            t.Tests.KeySpec | None,
            Field(default=None, description="Mapping has all keys"),
        ]
        lacks_keys: Annotated[
            t.Tests.KeySpec | None,
            Field(default=None, description="Mapping missing keys"),
        ]
        values: Annotated[
            Sequence[t.Tests.TestobjectSerializable] | None,
            Field(default=None, description="Mapping has all values"),
        ]
        kv: Annotated[
            t.Tests.KeyValueSpec | None,
            Field(default=None, description="Key-value pairs"),
        ]
        attrs: Annotated[
            t.Tests.AttributeSpec | None,
            Field(default=None, description="Object has attribute(s)"),
        ]
        methods: Annotated[
            t.Tests.AttributeSpec | None,
            Field(default=None, description="Object has method(s)"),
        ]
        attr_eq: Annotated[
            t.Tests.AttributeValueSpec | None,
            Field(default=None, description="Attribute equals"),
        ]
        ok: Annotated[
            bool | None,
            Field(default=None, description="For r: assert success"),
        ]
        error: Annotated[
            str | t.StrSequence | None,
            Field(default=None, description="For r: error contains"),
        ]
        deep: Annotated[
            t.Tests.DeepSpec | None,
            Field(default=None, description="Deep structural matching"),
        ]
        where: Annotated[
            t.Tests.PredicateSpec | None,
            Field(default=None, description="Custom predicate function"),
        ]

        @model_validator(mode="after")
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

        model_config: ClassVar[ConfigDict] = ConfigDict(populate_by_name=True)

        settings: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable] | None,
            Field(default=None, description="Initial configuration values"),
        ]
        container: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable] | None,
            Field(default=None, description="Initial container/service mappings"),
        ]
        context: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable] | None,
            Field(default=None, description="Initial context values"),
        ]
        cleanup: Annotated[
            t.Tests.CleanupSpec | None,
            Field(default=None, description="Cleanup functions"),
        ]
        env: Annotated[
            t.Tests.EnvironmentSpec | None,
            Field(default=None, description="Temporary environment variables"),
        ]
        cwd: Annotated[
            Path | str | None,
            Field(default=None, description="Temporary working directory"),
        ]

        @field_validator("cwd", mode="before")
        @classmethod
        def convert_cwd(cls, value: Path | str | None) -> Path | str | None:
            if isinstance(value, str):
                return Path(value)
            return value

    class DeepMatchResult(FlextModels.Value):
        """Structured output for deep-match comparisons."""

        path: Annotated[
            str,
            Field(description="Path where match occurred or failed"),
        ]
        expected: Annotated[
            t.Tests.TestobjectSerializable
            | Callable[[t.Tests.Testobject], bool]
            | None,
            Field(description="Expected value or predicate"),
        ]
        actual: Annotated[
            t.Tests.TestobjectSerializable | None,
            Field(default=None, description="Actual value found"),
        ]
        matched: Annotated[bool, Field(description="Whether match succeeded")]
        reason: Annotated[
            str,
            Field(default="", description="Reason for match failure"),
        ]

    class Validate:
        """Centralized TypeAdapters for test data validation.

        All TypeAdapters used across flext_tests modules are defined here.
        Access via m.Tests.Validate.* with flat aliases.
        """

        DICT_ADAPTER: ClassVar[
            TypeAdapter[Mapping[str, t.Tests.TestobjectSerializable]]
        ] = t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER
        LIST_ADAPTER: ClassVar[
            TypeAdapter[Sequence[t.Tests.TestobjectSerializable]]
        ] = t.Tests.TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER

    class Chain[TResult](FlextModels.Value):
        """Container for chained result assertions."""

        result: Annotated[
            r[TResult] | p.Result[TResult],
            Field(description="r being chained"),
        ]

    class TestScope(FlextModels.ArbitraryTypesModel):
        """Scope container for test configuration and runtime state."""

        __test__ = False

        settings: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable],
            Field(description="Configuration dictionary"),
        ] = Field(default_factory=dict)
        container: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable],
            Field(description="Container/service mappings"),
        ] = Field(default_factory=dict)
        context: Annotated[
            Mapping[str, t.Tests.TestobjectSerializable],
            Field(description="Context values"),
        ] = Field(default_factory=dict)
