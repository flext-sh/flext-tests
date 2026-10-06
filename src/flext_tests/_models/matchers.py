"""Matcher parameter models for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from collections.abc import Callable, Mapping, MutableMapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Annotated, ClassVar, TypeAliasType, cast

from _pytest.python_api import ApproxBase  # ruff: ignore[import-private-name] -- ApproxBase has no public pytest path in the supported versions; justified per fleet suppression law.
from flext_cli import m, u

from flext_tests import t
from flext_tests._models.base import FlextTestsFlextModelsBase
from flext_tests._utilities.payload import FlextTestsPayloadUtilities

if TYPE_CHECKING:
    from flext_tests import p


type _OwnedEntries = Mapping[
    str,
    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
    | Callable[[t.Tests.NativeMatchValue], bool],
]


class FlextTestsMatchersModelsMixin:
    """Matcher model group (result, that, scope, and chain parameters)."""

    # Namespace pinning: nested pydantic models capture THIS class-body frame
    # as their parent namespace at creation, and it cannot see module globals.
    # The facade letters used inside field annotations must therefore be bound
    # here, before the first nested model — keeping every declaration strictly
    # resolved with no deferred schemas and no ``model_rebuild``. (``p`` is
    # annotation-only, lives under ``TYPE_CHECKING``, and never enters the
    # schema namespace.)
    t = t
    m = m
    u = u

    # Matcher type aliases live in the class body (the namespace-class
    # convention): nested pydantic models capture the enclosing class-body
    # frame as their parent namespace, so declarations stay strictly resolved
    # at class creation — no deferred schemas, no ``model_rebuild``.
    type MatchExpectedValue = (
        FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
        | ApproxBase
        | TypeAliasType
        | None
    )
    type DeepExpected = (
        FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
        | Callable[[t.Tests.NativeMatchValue], bool]
        | str
        | None
    )

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
            if value is None or isinstance(value, ApproxBase | TypeAliasType):
                return value
            return FlextTestsPayloadUtilities.to_payload(
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
        ) -> (
            Mapping[str, FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload]
            | None
        ):
            """Own mapping leaves without changing native model identity.

            Returns:
                The resulting ``Mapping[str, FlextTestsBaseModelsMixin.Payload] |
                    None``.

            Raises:
                ValueError: If Matcher mapping requires a mapping payload.
            """
            if value is None:
                return None
            node = FlextTestsPayloadUtilities.to_payload(
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
        ) -> (
            tuple[FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload, ...]
            | None
        ):
            """Own sequence value expectations.

            Returns:
                The resulting ``tuple[FlextTestsBaseModelsMixin.Payload, ...] | None``.

            Raises:
                ValueError: If Matcher values require a sequence payload.
            """
            if value is None:
                return None
            node = FlextTestsPayloadUtilities.to_payload(
                value,
            )
            if node.kind in {"atom", "mapping"}:
                msg = "Matcher values require a sequence payload"
                raise ValueError(msg)
            return node.items

        @m.field_validator("deep", mode="before", check_fields=False)
        @classmethod
        def own_deep[ValueT](
            cls,
            value: Mapping[str, ValueT] | None,
        ) -> (
            Mapping[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
                | Callable[[t.Tests.NativeMatchValue], bool],
            ]
            | None
        ):
            """Keep predicates executable and own literal deep expectations.

            Returns:
                The resulting ``Mapping[str, FlextTestsBaseModelsMixin.Payload |
                    Callable[[t.Tests.NativeMatchValue], bool]] | None``.
            """
            if value is None:
                return None
            return cast(
                "_OwnedEntries",
                {
                    key: item
                    if callable(item)
                    else FlextTestsPayloadUtilities.to_payload(item)
                    for key, item in value.items()
                },
            )

    class MatchRule(PayloadParams):
        """One matcher rule parsed from a scalar, type, predicate, or mapping."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
            frozen=True,
            arbitrary_types_allowed=True,
            populate_by_name=True,
        )

        eq: Annotated[
            MatchExpectedValue,
            u.Field(description="Expected equality value."),
        ] = None
        ne: Annotated[
            MatchExpectedValue,
            u.Field(description="Expected inequality value."),
        ] = None
        is_: Annotated[
            type | t.VariadicTuple[type] | None,
            u.Field(
                validation_alias=t.AliasChoices("is_", "is"),
                description="Expected runtime type.",
            ),
        ] = None
        has: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(description="Required contained value."),
        ] = None
        lacks: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Forbidden contained value.",
            ),
        ] = None
        none: Annotated[bool | None, u.Field(description="Expected null state.")] = None
        empty: Annotated[bool | None, u.Field(description="Expected empty state.")] = (
            None
        )
        gt: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Exclusive lower bound."),
        ] = None
        gte: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Inclusive lower bound."),
        ] = None
        lt: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Exclusive upper bound."),
        ] = None
        lte: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Inclusive upper bound."),
        ] = None
        starts: Annotated[
            str | None,
            u.Field(description="Required string prefix."),
        ] = None
        ends: Annotated[str | None, u.Field(description="Required string suffix.")] = (
            None
        )
        match: Annotated[
            t.RegexPattern | None,
            u.Field(description="Required regular expression."),
        ] = None
        len: Annotated[
            t.Tests.LengthSpec | None,
            u.Field(description="Required length."),
        ] = None
        where: Annotated[
            Callable[[t.Tests.NativeMatchValue], bool] | None,
            u.Field(description="Predicate applied to the subject."),
        ] = None
        msg: Annotated[
            str | None,
            u.Field(description="Inherited assertion message."),
        ] = None

        @classmethod
        def parse(
            cls,
            value: p.AttributeProbe,
        ) -> MatchRule:
            """Parse one public matcher rule into its nominal representation.

            Returns:
                The resulting ``FlextTestsMatchersModelsMixin.MatchRule``.
            """
            if isinstance(value, cls):
                return value
            if isinstance(value, Mapping):
                mapping_value: Mapping[str, object] = value
                rule_keys = frozenset({*cls.model_fields, "is", "excludes"})
                if mapping_value and set(mapping_value).issubset(rule_keys):
                    return cls.model_validate(dict(mapping_value))
                # Own the mapping operand here; own_operand is idempotent, so
                # the field validator re-running on the owned payload is a no-op.
                return cls(eq=cls.own_operand(mapping_value))
            if isinstance(value, (type, tuple)):
                candidates = (value,) if isinstance(value, type) else tuple(value)
                members = tuple(item for item in candidates if isinstance(item, type))
                if len(members) == len(candidates):
                    # A bare type keeps its nominal form; a tuple of types
                    # narrows to the type members the rule accepts.
                    is_spec = members[0] if len(members) == 1 else members
                    return cls(is_=is_spec)
            if callable(value):
                return cls(
                    where=cast(
                        "Callable[[t.Tests.NativeMatchValue], bool]",
                        value,
                    ),
                )
            return cls(eq=cls.own_operand(value))

        @classmethod
        def parse_rule_fields(
            cls,
            value: p.AttributeProbe,
        ) -> p.AttributeProbe | Mapping[str, MatchRule] | Sequence[MatchRule] | None:
            """Parse paths, items, and attribute rule collections before validation.

            Returns:
                The resulting ``p.AttributeProbe | Mapping[str,
                    FlextTestsMatchersModelsMixin.MatchRule] |
                    Sequence[MatchRule] | None``.
            """
            if value is None:
                return None
            if isinstance(value, Mapping):
                return {key: cls.parse(rule) for key, rule in value.items()}
            if isinstance(value, Sequence) and not isinstance(value, str | bytes):
                return [cls.parse(rule) for rule in value]
            return value

    class OkParams(PayloadParams):
        """Matcher parameters for successful result assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
        )

        eq: Annotated[MatchExpectedValue, u.Field(description="Expected value.")] = None
        ne: Annotated[
            MatchExpectedValue,
            u.Field(description="Value must not equal."),
        ] = None
        is_: Annotated[
            type | t.VariadicTuple[type] | None,
            u.Field(
                validation_alias=t.AliasChoices("is_", "is"),
                description="Runtime type check.",
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
            u.Field(description="Greater than or equal."),
        ] = None
        lt: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Less than."),
        ] = None
        lte: Annotated[
            t.Tests.ComparableScalar | None,
            u.Field(description="Less than or equal."),
        ] = None
        has: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(description="Unified containment check."),
        ] = None
        lacks: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(description="Unified non-containment check."),
        ] = None
        starts: Annotated[
            str | None,
            u.Field(description="String starts with prefix."),
        ] = None
        ends: Annotated[str | None, u.Field(description="String ends with suffix.")] = (
            None
        )
        match: Annotated[
            t.RegexPattern | None,
            u.Field(description="Compiled regex pattern."),
        ] = None
        len: Annotated[
            t.Tests.LengthSpec | None,
            u.Field(description="Length spec."),
        ] = None
        deep: Annotated[
            Mapping[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
                | Callable[[t.Tests.NativeMatchValue], bool],
            ]
            | None,
            u.Field(description="Deep structural matching."),
        ] = None
        path: Annotated[
            t.Tests.PathSpec | None,
            u.Field(description="Extract nested value via dot notation."),
        ] = None
        paths: Annotated[
            Mapping[str, MatchRule] | None,
            u.Field(description="Multiple path-based assertions."),
        ] = None
        items: Annotated[
            Sequence[MatchRule] | Mapping[str | int, MatchRule] | None,
            u.Field(description="Sequence item assertions by selector."),
        ] = None
        attrs_match: Annotated[
            Mapping[str, MatchRule] | None,
            u.Field(description="Attribute assertions by attribute path."),
        ] = None
        where: Annotated[
            Callable[[t.Tests.NativeMatchValue], bool] | None,
            u.Field(description="Custom predicate function."),
        ] = None
        msg: Annotated[str | None, u.Field(description="Custom error message.")] = None

        @m.field_validator("paths", "items", "attrs_match", mode="before")
        @classmethod
        def parse_rules(
            cls,
            value: p.AttributeProbe,
        ) -> p.AttributeProbe | Mapping[str, MatchRule] | Sequence[MatchRule] | None:
            """Parse public rule collections into nominal rules.

            Returns:
                The resulting ``p.AttributeProbe | Mapping[str,
                    FlextTestsMatchersModelsMixin.MatchRule] |
                    Sequence[MatchRule] | None``.
            """
            return FlextTestsMatchersModelsMixin.MatchRule.parse_rule_fields(value)

    class FailParams(m.Value):
        """Matcher parameters for failure result assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        msg: Annotated[str | None, u.Field(description="Custom error message.")] = None
        has: Annotated[
            t.Tests.ExclusionSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("has", "contains"),
                description="Error contains substrings.",
            ),
        ] = None
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            u.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Error does not contain substrings.",
            ),
        ] = None
        starts: Annotated[
            str | None,
            u.Field(description="Error starts with prefix."),
        ] = None
        ends: Annotated[str | None, u.Field(description="Error ends with suffix.")] = (
            None
        )
        match: Annotated[
            t.RegexPattern | None,
            u.Field(description="Error matches compiled regex."),
        ] = None
        code: Annotated[str | None, u.Field(description="Error code equals.")] = None
        code_has: Annotated[
            t.Tests.ErrorCodeSpec | None,
            u.Field(description="Error code contains substrings."),
        ] = None
        data: Annotated[
            Mapping[str, FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload]
            | None,
            u.Field(description="Error data contains key-value pairs."),
        ] = None

        @m.field_validator("data", mode="before")
        @classmethod
        def own_data(
            cls,
            value: p.AttributeProbe,
        ) -> (
            Mapping[str, FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload]
            | None
        ):
            """Own expected error data through the shared mapping owner.

            Returns:
                The resulting ``Mapping[str, FlextTestsBaseModelsMixin.Payload] |
                    None``.
            """
            return FlextTestsMatchersModelsMixin.PayloadParams.own_mapping(value)

    class ThatParams(PayloadParams):
        """Generic matcher parameters for value assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(
            populate_by_name=True,
            arbitrary_types_allowed=True,
        )

        msg: Annotated[str | None, u.Field(description="Message.")] = None
        eq: Annotated[MatchExpectedValue, u.Field(description="Equals.")] = None
        ne: Annotated[MatchExpectedValue, u.Field(description="Not equals.")] = None
        is_: Annotated[
            type | t.VariadicTuple[type] | None,
            u.Field(validation_alias=t.AliasChoices("is_", "is"), description="Type."),
        ] = None
        not_: Annotated[
            type | t.VariadicTuple[type] | None,
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
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(
                validation_alias=t.AliasChoices("has", "contains"),
                description="Contains.",
            ),
        ] = None
        lacks: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(
                validation_alias=t.AliasChoices("lacks", "excludes"),
                description="Lacks.",
            ),
        ] = None
        starts: Annotated[str | None, u.Field(description="Prefix.")] = None
        ends: Annotated[str | None, u.Field(description="Suffix.")] = None
        match: Annotated[t.RegexPattern | None, u.Field(description="Regex.")] = None
        first: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(description="First item."),
        ] = None
        last: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(description="Last item."),
        ] = None
        all_: Annotated[
            type | Callable[[t.Tests.NativeMatchValue], bool] | None,
            u.Field(validation_alias=t.AliasChoices("all_", "all"), description="All."),
        ] = None
        any_: Annotated[
            type | Callable[[t.Tests.NativeMatchValue], bool] | None,
            u.Field(validation_alias=t.AliasChoices("any_", "any"), description="Any."),
        ] = None
        sorted: Annotated[
            bool
            | Callable[[t.Tests.NativeMatchValue], t.Tests.NativeMatchValue]
            | None,
            u.Field(description="Sort key."),
        ] = None
        unique: Annotated[bool | None, u.Field(description="Unique.")] = None
        keys: Annotated[t.Tests.KeySpec | None, u.Field(description="Keys.")] = None
        lacks_keys: Annotated[
            t.Tests.KeySpec | None,
            u.Field(description="No keys."),
        ] = None
        values: Annotated[
            t.SequenceOf[FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload]
            | None,
            u.Field(description="Values."),
        ] = None
        kv: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
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
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(description="Attr equals."),
        ] = None
        ok: Annotated[bool | None, u.Field(description="Result ok.")] = None
        error: Annotated[
            str | t.StrSequence | None,
            u.Field(description="Result error."),
        ] = None
        deep: Annotated[
            Mapping[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
                | Callable[[t.Tests.NativeMatchValue], bool],
            ]
            | None,
            u.Field(description="Deep spec."),
        ] = None
        paths: Annotated[
            Mapping[str, MatchRule] | None,
            u.Field(description="Paths."),
        ] = None
        items: Annotated[
            Sequence[MatchRule] | Mapping[str | int, MatchRule] | None,
            u.Field(description="Items."),
        ] = None
        attrs_match: Annotated[
            Mapping[str, MatchRule] | None,
            u.Field(description="Attr rules."),
        ] = None
        where: Annotated[
            Callable[[t.Tests.NativeMatchValue], bool] | None,
            u.Field(description="Predicate."),
        ] = None

        @m.field_validator("paths", "items", "attrs_match", mode="before")
        @classmethod
        def parse_rules(
            cls,
            value: p.AttributeProbe,
        ) -> p.AttributeProbe | Mapping[str, MatchRule] | Sequence[MatchRule] | None:
            """Parse public rule collections into nominal rules.

            Returns:
                The resulting ``p.AttributeProbe | Mapping[str,
                    FlextTestsMatchersModelsMixin.MatchRule] |
                    Sequence[MatchRule] | None``.
            """
            return FlextTestsMatchersModelsMixin.MatchRule.parse_rule_fields(value)

        @m.model_validator(mode="after")
        def normalize_legacy_parameters(
            self,
        ) -> FlextTestsMatchersModelsMixin.ThatParams:
            """Normalize legacy aliases into canonical matcher fields.

            Returns:
                The resulting ``FlextTestsMatchersModelsMixin.ThatParams``.
            """
            # Why: precise union of the two fields actually assigned below
            # ("has" <- self.error: str | StrSequence; "len" <- LengthSpec
            # tuple); TestobjectSerializable rejected tuple[int, int] once the
            # recursive-alias fix made mypy/pyrefly evaluate it for real.
            updates: MutableMapping[
                str,
                t.Tests.LengthSpec
                | FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
                | None,
            ] = {}
            if self.error is not None and self.has is None:
                # self.error is a non-None native sequence/scalar, so owning it
                # is exactly the payload walker; no approx/type operand applies.
                updates["has"] = FlextTestsPayloadUtilities.to_payload(
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

    class ScopeParams(PayloadParams):
        """Parameters for temporary test scope configuration."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        settings: Annotated[
            t.MappingKV[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
            ]
            | None,
            u.Field(description="Initial configuration values."),
        ] = None
        container: Annotated[
            t.MappingKV[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
            ]
            | None,
            u.Field(description="Initial container/service mappings."),
        ] = None
        context: Annotated[
            t.MappingKV[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
            ]
            | None,
            u.Field(description="Initial context values."),
        ] = None
        cleanup: Annotated[
            t.Tests.CleanupSpec | None,
            u.Field(description="Cleanup functions."),
        ] = None
        env: Annotated[
            t.Tests.EnvironmentSpec | None,
            u.Field(description="Temporary environment variables."),
        ] = None
        remove_env_keys: Annotated[
            t.StrSequence,
            u.Field(description="Environment variables absent inside the scope."),
        ] = ()
        python_paths: Annotated[
            t.StrSequence,
            u.Field(description="Import roots prepended inside the scope."),
        ] = ()
        cwd: Annotated[
            Path | str | None,
            u.Field(description="Temporary working directory."),
        ] = None

        @m.field_validator("cwd", mode="before")
        @classmethod
        def convert_cwd(cls, value: Path | str | None) -> Path | str | None:
            """Convert string cwd to Path.

            Returns:
                The resulting ``Path | str | None``.
            """
            if isinstance(value, str):
                return Path(value)
            return value

    class DeepMatchResult(m.Value):
        """Structured output for deep-match comparisons."""

        path: Annotated[str, u.Field(description="Path where matching occurred.")]
        expected: Annotated[
            DeepExpected,
            u.Field(description="Expected value or predicate."),
        ]
        actual: Annotated[
            FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload | None,
            u.Field(description="Actual value found."),
        ] = None
        matched: Annotated[bool, u.Field(description="Whether match succeeded.")]
        reason: Annotated[str, u.Field(description="Reason for match failure.")] = ""

    class Chain[TResult](m.Value):
        """Container for chained result assertions."""

        result: Annotated[
            p.Result[TResult],
            u.Field(description="Result being chained."),
        ]

    class TestScope(PayloadParams):
        """Scope container for test configuration and runtime state."""

        settings: Annotated[
            t.MappingKV[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
            ],
            u.Field(description="Configuration dictionary."),
        ] = u.Field(
            default_factory=lambda: MappingProxyType(
                dict[
                    str,
                    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
                ](),
            ),
        )
        container: Annotated[
            t.MappingKV[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
            ],
            u.Field(description="Container/service mappings."),
        ] = u.Field(
            default_factory=lambda: MappingProxyType(
                dict[
                    str,
                    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
                ](),
            ),
        )
        context: Annotated[
            t.MappingKV[
                str,
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
            ],
            u.Field(description="Context values."),
        ] = u.Field(
            default_factory=lambda: MappingProxyType(
                dict[
                    str,
                    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
                ](),
            ),
        )


__all__: list[str] = ["FlextTestsMatchersModelsMixin"]
