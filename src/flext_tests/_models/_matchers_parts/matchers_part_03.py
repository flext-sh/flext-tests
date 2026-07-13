"""Matcher support models for flext-tests."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, ClassVar

from flext_infra import m, u
from flext_tests import p, t
from flext_tests._models._matchers_parts.matchers_part_02 import (
    FlextTestsMatchersModelsMixin as FlextTestsMatchersModelsMixinPart02,
)


class FlextTestsMatchersModelsMixin(FlextTestsMatchersModelsMixinPart02):
    """Matcher support models for flext-tests."""

    class ScopeParams(m.Value):
        """Parameters for temporary test scope configuration."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        settings: Annotated[
            t.MappingKV[str, t.Tests.TestobjectSerializable] | None,
            u.Field(description="Initial configuration values."),
        ] = None
        container: Annotated[
            t.MappingKV[str, t.Tests.TestobjectSerializable] | None,
            u.Field(description="Initial container/service mappings."),
        ] = None
        context: Annotated[
            t.MappingKV[str, t.Tests.TestobjectSerializable] | None,
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
        cwd: Annotated[
            Path | str | None,
            u.Field(description="Temporary working directory."),
        ] = None

        @u.field_validator("cwd", mode="before")
        @classmethod
        def convert_cwd(cls, value: Path | str | None) -> Path | str | None:
            """Convert string cwd to Path."""
            if isinstance(value, str):
                return Path(value)
            return value

    class DeepMatchResult(m.Value):
        """Structured output for deep-match comparisons."""

        path: Annotated[str, u.Field(description="Path where matching occurred.")]
        expected: Annotated[
            t.Tests.TestobjectSerializable
            | Callable[[t.Tests.Testobject], bool]
            | None,
            u.Field(description="Expected value or predicate."),
        ]
        actual: Annotated[
            t.Tests.TestobjectSerializable | None,
            u.Field(description="Actual value found."),
        ] = None
        matched: Annotated[bool, u.Field(description="Whether match succeeded.")]
        reason: Annotated[str, u.Field(description="Reason for match failure.")] = ""

    class Validate:
        """Centralized TypeAdapters for test data validation."""

        DICT_ADAPTER: ClassVar[
            m.TypeAdapter[Mapping[str, t.Tests.TestobjectSerializable]]
        ] = t.Tests.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER
        LIST_ADAPTER: ClassVar[
            m.TypeAdapter[Sequence[t.Tests.TestobjectSerializable]]
        ] = t.Tests.TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER

    class Chain[TResult](m.Value):
        """Container for chained result assertions."""

        result: Annotated[
            p.Result[TResult],
            u.Field(description="Result being chained."),
        ]

    class TestScope(m.ArbitraryTypesModel):
        """Scope container for test configuration and runtime state."""

        settings: Annotated[
            t.MappingKV[str, t.Tests.TestobjectSerializable],
            u.Field(description="Configuration dictionary."),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
        container: Annotated[
            t.MappingKV[str, t.Tests.TestobjectSerializable],
            u.Field(description="Container/service mappings."),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
        context: Annotated[
            t.MappingKV[str, t.Tests.TestobjectSerializable],
            u.Field(description="Context values."),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))


__all__: list[str] = ["FlextTestsMatchersModelsMixin"]
