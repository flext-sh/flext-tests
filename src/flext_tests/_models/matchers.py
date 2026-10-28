"""Matcher parameter models for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping, MutableMapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, ClassVar, Self, TypeAliasType, cast

from flext_cli import m

from flext_tests import c, p, t
from flext_tests._models import FlextTestsModelsBase
from flext_tests._utilities import FlextTestsUtilitiesPayload

type MatchExpectedValue = (
    FlextTestsModelsBase.Payload
    | t.Port[p.Tests.ApproxLike]
    | t.Port[TypeAliasType]
    | None
)
type DeepExpected = (
    FlextTestsModelsBase.Payload
    | Callable[[p.Tests.NativeMatchValue], bool]
    | str
    | None
)


type _OwnedEntries = Mapping[
    str,
    FlextTestsModelsBase.Payload | Callable[[p.Tests.NativeMatchValue], bool],
]


class FlextTestsModelsMatchers:
    """Matcher model group (result, that, scope, and chain parameters)."""

    type DeepSpec = Mapping[
        str,
        FlextTestsModelsBase.Payload | Callable[[p.Tests.NativeMatchValue], bool],
    ]

    class PayloadParams(m.Value):
        """Own matcher operand trees once at parameter ingress."""

        @m.field_validator(
            "eq",
            "ne",
            "has",
            "lacks",
            "first",
            "last",
            "kv",
            "attr_eq",
            mode="before",
            check_fields=False,
        )
        @classmethod
        def own_operand(cls, value: p.AttributeProbe) -> MatchExpectedValue:
            """Preserve explicit matcher operators and own native operands.

            Returns:
                The resulting ``MatchExpectedValue``.

            """
            if value is None or isinstance(value, p.Tests.ApproxLike | TypeAliasType):
                return value
            return FlextTestsUtilitiesPayload.to_payload(
                value,
            )

        @m.field_validator(
            "settings",
            "container",
            "context",
            "data",
            mode="before",
            check_fields=False,
        )
        @classmethod
        def own_mapping(
            cls,
            value: p.AttributeProbe,
        ) -> Mapping[str, FlextTestsModelsBase.Payload] | None:
            """Own mapping leaves without changing native model identity.

            Returns:
                The resulting ``Mapping[str,.Payload] |
                    None``.

            Raises:
                ValueError: If Matcher mapping requires a mapping payload.

            """
            if value is None:
                return None
            node = FlextTestsUtilitiesPayload.to_payload(
                value,
            )
            if node.kind != "mapping":
                msg = "Matcher mapping requires a mapping payload"
                raise ValueError(msg)
            return node.entries

        @m.field_validator("values", mode="before", check_fields=False)
        @classmethod
        def own_values(
            cls,
            value: p.AttributeProbe,
        ) -> tuple[FlextTestsModelsBase.Payload, ...] | None:
            """Own sequence value expectations.

            Returns:
                The resulting ``tuple.Payload, ...] | None``.

            Raises:
                ValueError: If Matcher values require a sequence payload.

            """
            if value is None:
                return None
            node = FlextTestsUtilitiesPayload.to_payload(
                value,
            )
            if node.kind in {"atom", "mapping"}:
                msg = "Matcher values require a sequence payload"
                raise ValueError(msg)
            return node.items

        @m.field_validator(c.MergeStrategy.DEEP, mode="before", check_fields=False)
        @classmethod
        def own_deep[ValueT](
            cls,
            value: Mapping[str, ValueT] | None,
        ) -> (
            Mapping[
                str,
                FlextTestsModelsBase.Payload
                | Callable[[p.Tests.NativeMatchValue], bool],
            ]
            | None
        ):
            """Keep predicates executable and own literal deep expectations.

            Returns:
                The resulting ``Mapping[str,.Payload |
                    Callable[[p.Tests.NativeMatchValue], bool]] | None``.

            """
            if value is None:
                return None
            return cast(
                "_OwnedEntries",
                {
                    key: item
                    if callable(item)
                    else FlextTestsUtilitiesPayload.to_payload(item)
                    for key, item in value.items()
                },
            )

        @m.field_validator(
            "paths",
            "items",
            mode="before",
            check_fields=False,
        )
        @classmethod
        def parse_rules(
            cls,
            value: p.AttributeProbe,
        ) -> (
            p.AttributeProbe
            | Mapping[str, FlextTestsModelsMatchers.MatchRule]
            | Sequence[FlextTestsModelsMatchers.MatchRule]
            | None
        ):
            """Parse public rule collections into nominal rules.

            Returns:
                The resulting ``p.AttributeProbe | Mapping[str,
                    FlextTestsModelsMatchers.MatchRule] |
                    Sequence[FlextTestsModelsMatchers.MatchRule] | None``.

            """
            return FlextTestsModelsMatchers.MatchRule.parse_rule_fields(value)

        @m.field_validator("attrs_match", mode="before", check_fields=False)
        @classmethod
        def parse_attribute_rules(
            cls,
            value: p.AttributeProbe,
        ) -> p.AttributeProbe:
            """Parse rules whose callbacks receive unchanged attribute values.

            Returns:
                Rules parameterized by the original attribute capability.

            """
            return FlextTestsModelsMatchers.MatchRule[
                p.AttributeProbe
            ].parse_rule_fields(value)

    class MatchRule[SubjectT = p.Tests.NativeMatchValue](PayloadParams):
        """One matcher rule parsed from a scalar, type, predicate, or mapping."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
            frozen=True,
            populate_by_name=True,
        )

        eq: Annotated[
            MatchExpectedValue,
            m.Field(description="Expected equality value."),
        ] = None
        ne: Annotated[
            MatchExpectedValue,
            m.Field(description="Expected inequality value."),
        ] = None
        is_: Annotated[
            type | t.VariadicTuple[type] | None,
            m.Field(
                validation_alias=t.AliasChoices("is_", "is"),
                description="Expected runtime type.",
            ),
        ] = None
        has: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(description="Required contained value."),
        ] = None
        lacks: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Forbidden contained value.",
            ),
        ] = None
        none: Annotated[bool | None, m.Field(description="Expected null state.")] = None
        empty: Annotated[bool | None, m.Field(description="Expected empty state.")] = (
            None
        )
        gt: Annotated[
            t.Tests.ComparableScalar | None,
            m.Field(description="Exclusive lower bound."),
        ] = None
        gte: Annotated[
            t.Tests.ComparableScalar | None,
            m.Field(description="Inclusive lower bound."),
        ] = None
        lt: Annotated[
            t.Tests.ComparableScalar | None,
            m.Field(description="Exclusive upper bound."),
        ] = None
        lte: Annotated[
            t.Tests.ComparableScalar | None,
            m.Field(description="Inclusive upper bound."),
        ] = None
        starts: Annotated[
            str | None,
            m.Field(description="Required string prefix."),
        ] = None
        ends: Annotated[str | None, m.Field(description="Required string suffix.")] = (
            None
        )
        match: Annotated[
            t.RegexPattern | None,
            m.Field(description="Required regular expression."),
        ] = None
        len: Annotated[
            t.Tests.LengthSpec | None,
            m.Field(description="Required length."),
        ] = None
        where: Annotated[
            Callable[[SubjectT], bool] | None,
            m.Field(description="Predicate applied to the subject."),
        ] = None
        msg: Annotated[
            str | None,
            m.Field(description="Inherited assertion message."),
        ] = None

        @classmethod
        def parse_type_tuple(
            cls,
            value: p.AttributeProbe,
        ) -> Self:
            """Parse a tuple operand into its nominal type-membership rule.

            Returns:
                The resulting ``FlextTestsMatchers.MatchRule``.

            """
            candidates = tuple(cast("Sequence[object]", value))
            members = tuple(item for item in candidates if isinstance(item, type))
            if len(members) == len(candidates):
                # A tuple of types narrows to the type members the rule accepts.
                is_spec = members[0] if len(members) == 1 else members
                return cls(is_=is_spec)
            # A non-type tuple is its own operand: tuples are never callable,
            # so the remaining arms collapse to the equality arm.
            return cls(eq=cls.own_operand(cast("Sequence[object]", value)))

        @classmethod
        def parse(
            cls,
            value: p.AttributeProbe,
        ) -> Self:
            """Parse one public matcher rule into its nominal representation.

            Returns:
                The resulting ``FlextTestsMatchers.MatchRule``.

            """
            if isinstance(value, cls):
                return value
            if isinstance(value, Mapping):
                return cls.parse_mapping(cast("t.JsonMapping", value))
            if isinstance(value, tuple):
                return cls.parse_type_tuple(cast("tuple[object, ...]", value))
            if isinstance(value, type):
                # A bare type keeps its nominal form.
                return cls(is_=value)
            if callable(value):
                return cls.model_validate({"where": value})
            return cls(eq=cls.own_operand(value))

        @classmethod
        def parse_mapping(
            cls,
            value: p.AttributeProbe,
        ) -> Self:
            """Parse a mapping operand into a validated or owned-equality rule.

            Returns:
                The resulting ``FlextTestsMatchers.MatchRule``.

            """
            mapping_value = cast("t.JsonMapping", value)
            rule_keys = frozenset({*cls.model_fields, "is", "excludes"})
            if mapping_value and set(mapping_value).issubset(rule_keys):
                return cls.model_validate(dict(mapping_value))
            # Own the mapping operand here; own_operand is idempotent, so
            # the field validator re-running on the owned payload is a no-op.
            return cls(eq=cls.own_operand(mapping_value))

        @classmethod
        def parse_rule_fields(
            cls,
            value: p.AttributeProbe,
        ) -> p.AttributeProbe | Mapping[str, Self] | Sequence[Self] | None:
            """Parse paths, items, and attribute rule collections before validation.

            Returns:
                The resulting ``p.AttributeProbe | Mapping[str,
                    FlextTestsModelsMatchers.MatchRule] |
                    Sequence[FlextTestsModelsMatchers.MatchRule] | None``.

            """
            if value is None:
                return None
            if isinstance(value, Mapping):
                return {
                    key: cls.parse(rule)
                    for key, rule in cast("t.JsonMapping", value).items()
                }
            if isinstance(value, Sequence) and not isinstance(value, str | bytes):
                return [cls.parse(rule) for rule in cast("Sequence[object]", value)]
            return value

    class FailParams(m.Value):
        """Matcher parameters for failure result assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        msg: Annotated[str | None, m.Field(description="Custom error message.")] = None
        has: Annotated[
            t.Tests.ExclusionSpec | None,
            m.Field(
                validation_alias=t.AliasChoices("has", "contains"),
                description="Error contains substrings.",
            ),
        ] = None
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            m.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Error does not contain substrings.",
            ),
        ] = None
        starts: Annotated[
            str | None,
            m.Field(description="Error starts with prefix."),
        ] = None
        ends: Annotated[str | None, m.Field(description="Error ends with suffix.")] = (
            None
        )
        match: Annotated[
            t.RegexPattern | None,
            m.Field(description="Error matches compiled regex."),
        ] = None
        code: Annotated[str | None, m.Field(description="Error code equals.")] = None
        code_has: Annotated[
            t.Tests.ErrorCodeSpec | None,
            m.Field(description="Error code contains substrings."),
        ] = None
        data: Annotated[
            Mapping[str, FlextTestsModelsBase.Payload] | None,
            m.Field(description="Error data contains key-value pairs."),
        ] = None

        @m.field_validator("data", mode="before")
        @classmethod
        def own_data(
            cls,
            value: p.AttributeProbe,
        ) -> Mapping[str, FlextTestsModelsBase.Payload] | None:
            """Own expected error data through the shared mapping owner.

            Returns:
                The resulting ``Mapping[str,.Payload] |
                    None``.

            """
            return FlextTestsModelsMatchers.PayloadParams.own_mapping(value)

    class ThatParams(PayloadParams):
        """Generic matcher parameters for value assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
            populate_by_name=True,
        )

        msg: Annotated[str | None, m.Field(description="Message.")] = None
        truth: Annotated[
            bool | None,
            m.Field(description="Native truth value of the original subject."),
        ] = None
        assertion_message: Annotated[
            t.Port[p.AttributeProbe] | None,
            m.Field(
                description=(
                    "Original assertion message, passed inside its failure branch."
                )
            ),
        ] = None
        is_: Annotated[
            type | t.VariadicTuple[type] | None,
            m.Field(validation_alias=t.AliasChoices("is_", "is"), description="Type."),
        ] = None
        not_: Annotated[
            type | t.VariadicTuple[type] | None,
            m.Field(
                validation_alias=t.AliasChoices("not_", "not"),
                description="Not type.",
            ),
        ] = None
        none: Annotated[bool | None, m.Field(description="None check.")] = None
        empty: Annotated[bool | None, m.Field(description="Empty check.")] = None
        gt: Annotated[
            t.Tests.ComparableScalar | None,
            m.Field(description="Greater than."),
        ] = None
        gte: Annotated[
            t.Tests.ComparableScalar | None,
            m.Field(description="Greater/equal."),
        ] = None
        lt: Annotated[
            t.Tests.ComparableScalar | None,
            m.Field(description="Less than."),
        ] = None
        lte: Annotated[
            t.Tests.ComparableScalar | None,
            m.Field(description="Less/equal."),
        ] = None
        len: Annotated[
            t.Tests.LengthSpec | None,
            m.Field(
                validation_alias=t.AliasChoices("len", "length"),
                description="Length.",
            ),
        ] = None
        length_gt: Annotated[int | None, m.Field(description="Length >.")] = None
        length_gte: Annotated[int | None, m.Field(description="Length >=.")] = None
        length_lt: Annotated[int | None, m.Field(description="Length <.")] = None
        length_lte: Annotated[int | None, m.Field(description="Length <=.")] = None
        has: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(
                validation_alias=t.AliasChoices("has", "contains"),
                description="Contains.",
            ),
        ] = None
        lacks: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Lacks.",
            ),
        ] = None
        starts: Annotated[str | None, m.Field(description="Prefix.")] = None
        ends: Annotated[str | None, m.Field(description="Suffix.")] = None
        match: Annotated[t.RegexPattern | None, m.Field(description="Regex.")] = None
        first: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(description="First item."),
        ] = None
        last: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(description="Last item."),
        ] = None
        all_: Annotated[
            type | Callable[[p.Tests.NativeMatchValue], bool] | None,
            m.Field(validation_alias=t.AliasChoices("all_", "all"), description="All."),
        ] = None
        any_: Annotated[
            type | Callable[[p.Tests.NativeMatchValue], bool] | None,
            m.Field(validation_alias=t.AliasChoices("any_", "any"), description="Any."),
        ] = None
        sorted: Annotated[
            bool
            | Callable[[p.Tests.NativeMatchValue], p.Tests.NativeMatchValue]
            | None,
            m.Field(description="Sort key."),
        ] = None
        unique: Annotated[bool | None, m.Field(description="Unique.")] = None
        keys: Annotated[t.Tests.KeySpec | None, m.Field(description="Keys.")] = None
        lacks_keys: Annotated[
            t.Tests.KeySpec | None,
            m.Field(description="No keys."),
        ] = None
        values: Annotated[
            t.SequenceOf[FlextTestsModelsBase.Payload] | None,
            m.Field(description="Values."),
        ] = None
        kv: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(description="Key-values."),
        ] = None
        attrs: Annotated[
            t.Tests.AttributeSpec | None,
            m.Field(description="Attrs."),
        ] = None
        methods: Annotated[
            t.Tests.AttributeSpec | None,
            m.Field(description="Methods."),
        ] = None
        attr_eq: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(description="Attr equals."),
        ] = None
        ok: Annotated[bool | None, m.Field(description="Result ok.")] = None
        error: Annotated[
            str | t.StrSequence | None,
            m.Field(description="Result error."),
        ] = None
        deep: Annotated[
            Mapping[
                str,
                FlextTestsModelsBase.Payload
                | Callable[[p.Tests.NativeMatchValue], bool],
            ]
            | None,
            m.Field(description="Deep spec."),
        ] = None
        paths: Annotated[
            Mapping[str, FlextTestsModelsMatchers.MatchRule] | None,
            m.Field(description="Paths."),
        ] = None
        items: Annotated[
            Sequence[FlextTestsModelsMatchers.MatchRule]
            | Mapping[str | int, FlextTestsModelsMatchers.MatchRule]
            | None,
            m.Field(description="Items."),
        ] = None
        attrs_match: Annotated[
            Mapping[str, FlextTestsModelsMatchers.MatchRule[p.AttributeProbe]] | None,
            m.Field(description="Attr rules."),
        ] = None
        where: Annotated[
            Callable[[p.Tests.NativeMatchValue], bool] | None,
            m.Field(description="Predicate."),
        ] = None

        @m.model_validator(mode="after")
        def normalize_legacy_parameters(
            self,
        ) -> FlextTestsModelsMatchers.ThatParams:
            """Normalize legacy aliases into canonical matcher fields.

            Returns:
                The resulting ``FlextTestsModelsMatchers.ThatParams``.

            Raises:
                ValueError: If legacy parameter normalization fails.

            """
            if "assertion_message" in self.model_fields_set and self.truth is None:
                message = "assertion_message requires the native truth criterion"
                raise ValueError(message)
            if self.truth is not None and self.model_fields_set.difference({
                "truth",
                "msg",
                "assertion_message",
            }):
                message = "native truth cannot be combined with payload criteria"
                raise ValueError(message)
            # Why: precise union of the two fields actually assigned below
            # ("has" <- self.error: str | StrSequence; "len" <- LengthSpec
            # tuple); TestobjectSerializable rejected tuple[int, int] once the
            # recursive-alias fix made mypy/pyrefly evaluate it for real.
            updates: MutableMapping[
                str,
                t.Tests.LengthSpec | FlextTestsModelsBase.Payload | None,
            ] = {}
            if self.error is not None and self.has is None:
                # self.error is a non-None native sequence/scalar, so owning it
                # is exactly the payload walker; no approx/type operand applies.
                updates["has"] = FlextTestsUtilitiesPayload.to_payload(
                    self.error,
                )
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

    class ScopeParams(m.Value):
        """Parameters for temporary test scope configuration."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
            populate_by_name=True,
        )

        settings: Annotated[
            t.MappingKV[
                str,
                t.Port[p.Tests.NativeMatchValue],
            ]
            | None,
            m.Field(description="Initial configuration values."),
        ] = None
        container: Annotated[
            t.MappingKV[
                str,
                t.Port[p.Tests.NativeMatchValue],
            ]
            | None,
            m.Field(description="Initial container/service mappings."),
        ] = None
        context: Annotated[
            t.MappingKV[
                str,
                t.Port[p.Tests.NativeMatchValue],
            ]
            | None,
            m.Field(description="Initial context values."),
        ] = None
        cleanup: Annotated[
            t.Tests.CleanupSpec | None,
            m.Field(description="Cleanup functions."),
        ] = None
        env: Annotated[
            t.Tests.EnvironmentSpec | None,
            m.Field(description="Temporary environment variables."),
        ] = None
        remove_env_keys: Annotated[
            t.StrSequence,
            m.Field(description="Environment variables absent inside the scope."),
        ] = ()
        python_paths: Annotated[
            t.StrSequence,
            m.Field(description="Import roots prepended inside the scope."),
        ] = ()
        cwd: Annotated[
            Path | str | None,
            m.Field(description="Temporary working directory."),
        ] = None

    class DeepMatchResult(m.Value):
        """Structured output for deep-match comparisons."""

        path: Annotated[str, m.Field(description="Path where matching occurred.")]
        expected: Annotated[
            DeepExpected,
            m.Field(description="Expected value or predicate."),
        ]
        actual: Annotated[
            FlextTestsModelsBase.Payload | None,
            m.Field(description="Actual value found."),
        ] = None
        matched: Annotated[bool, m.Field(description="Whether match succeeded.")]
        reason: Annotated[str, m.Field(description="Reason for match failure.")] = ""

    class Chain[TResult](m.Value):
        """Container for chained result assertions."""

        result: Annotated[
            t.Port[p.Result[TResult]],
            m.Field(exclude=True, description="Result being chained."),
        ]

    class TestScope(m.Value):
        """Scope container for test configuration and runtime state."""

        settings: Annotated[
            t.MappingKV[
                str,
                t.Port[p.Tests.NativeMatchValue],
            ],
            m.Field(description="Configuration dictionary."),
        ] = m.Field(
            default_factory=lambda: MappingProxyType(
                dict[
                    str,
                    p.Tests.NativeMatchValue,
                ](),
            ),
        )
        container: Annotated[
            t.MappingKV[
                str,
                t.Port[p.Tests.NativeMatchValue],
            ],
            m.Field(description="Container/service mappings."),
        ] = m.Field(
            default_factory=lambda: MappingProxyType(
                dict[
                    str,
                    p.Tests.NativeMatchValue,
                ](),
            ),
        )
        context: Annotated[
            t.MappingKV[
                str,
                t.Port[p.Tests.NativeMatchValue],
            ],
            m.Field(description="Context values."),
        ] = m.Field(
            default_factory=lambda: MappingProxyType(
                dict[
                    str,
                    p.Tests.NativeMatchValue,
                ](),
            ),
        )


__all__: list[str] = ["FlextTestsModelsMatchers"]
