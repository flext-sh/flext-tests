"""Result matcher parameter models for flext-tests."""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_cli import m, u
from flext_tests.typings import t


class FlextTestsMatchersModelsMixin:
    """Matcher model group for flext-tests."""

    class OkParams(m.Value):
        """Matcher parameters for successful result assertions."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        eq: Annotated[
            t.Tests.MatcherEqTarget | None,
            u.Field(description="Expected value."),
        ] = None
        ne: Annotated[
            t.Tests.MatcherEqTarget | None,
            u.Field(description="Value must not equal."),
        ] = None
        is_: Annotated[
            type | tuple[type, ...] | None,
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
            t.Tests.ContainmentSpec | None,
            u.Field(description="Unified containment check."),
        ] = None
        lacks: Annotated[
            t.Tests.ExclusionSpec | None,
            u.Field(description="Unified non-containment check."),
        ] = None
        starts: Annotated[
            str | None,
            u.Field(description="String starts with prefix."),
        ] = None
        ends: Annotated[
            str | None,
            u.Field(description="String ends with suffix."),
        ] = None
        match: Annotated[
            t.Infra.RegexPattern | None,
            u.Field(description="Compiled regex pattern."),
        ] = None
        len: Annotated[
            t.Tests.LengthSpec | None,
            u.Field(description="Length spec."),
        ] = None
        deep: Annotated[
            t.Tests.DeepSpec | None,
            u.Field(description="Deep structural matching."),
        ] = None
        path: Annotated[
            t.Tests.PathSpec | None,
            u.Field(description="Extract nested value via dot notation."),
        ] = None
        paths: Annotated[
            t.Tests.PathMatchSpec | None,
            u.Field(description="Multiple path-based assertions."),
        ] = None
        items: Annotated[
            t.Tests.ItemMatchSpec | None,
            u.Field(description="Sequence item assertions by selector."),
        ] = None
        attrs_match: Annotated[
            t.Tests.AttributeMatchSpec | None,
            u.Field(description="Attribute assertions by attribute path."),
        ] = None
        where: Annotated[
            t.Tests.PredicateSpec | None,
            u.Field(description="Custom predicate function."),
        ] = None
        msg: Annotated[str | None, u.Field(description="Custom error message.")] = None

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
        ends: Annotated[
            str | None,
            u.Field(description="Error ends with suffix."),
        ] = None
        match: Annotated[
            t.Infra.RegexPattern | None,
            u.Field(description="Error matches compiled regex."),
        ] = None
        code: Annotated[str | None, u.Field(description="Error code equals.")] = None
        code_has: Annotated[
            t.Tests.ErrorCodeSpec | None,
            u.Field(description="Error code contains substrings."),
        ] = None
        data: Annotated[
            t.Tests.ErrorDataSpec | None,
            u.Field(description="Error data contains key-value pairs."),
        ] = None


__all__: list[str] = ["FlextTestsMatchersModelsMixin"]
