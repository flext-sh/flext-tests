"""Type system foundation for FLEXT tests.

Provides FlextTestsTypes, extending t with test-specific type definitions
for test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from pathlib import Path
from typing import Literal, TypeAliasType, TypeIs

from flext_core import FlextProtocols, FlextTypes, m
from pydantic import BaseModel, InstanceOf

p = FlextProtocols

type _TestobjectSerializable = (
    t.Primitives
    | None
    | bytes
    | datetime
    | Path
    | BaseModel
    | type
    | frozenset[str]
    | Sequence[_TestobjectSerializable]
    | Mapping[str, _TestobjectSerializable]
)

type _Testobject = (
    _TestobjectSerializable
    | Exception
    | p.Logger
    | p.Container
    | Sequence[_Testobject]
    | Mapping[str, _Testobject]
)


class FlextTestsTypes(FlextTypes):
    """Type system foundation for FLEXT tests - extends t.

    Architecture: Extends t with test-specific type aliases and definitions.
    All base types from t are available through inheritance.
    """

    class Tests:
        """Test-specific type definitions namespace.

        All test-specific types organized under t.Tests.* pattern.
        """

        type Testobject = _Testobject
        type TestobjectSerializable = _TestobjectSerializable
        type object = _Testobject
        type FileContent = (
            str
            | bytes
            | Mapping[str, _Testobject]
            | Sequence[Sequence[str]]
            | InstanceOf[BaseModel]
        )
        type TestResultValue = _Testobject
        "Type for test result values."

        class Factory:
            """Factory-specific type definitions for test factories (tt)."""

            type ModelKind = Literal[
                "user",
                "config",
                "service",
                "entity",
                "value",
                "command",
                "query",
                "event",
            ]
            "Kind parameter for model() factory method."
            type ResultKind = Literal["ok", "fail", "from_value"]
            "Kind parameter for res() factory method."
            type OpKind = Literal[
                "simple",
                "add",
                "format",
                "error",
                "type_error",
                "result_ok",
                "result_fail",
            ]
            "Kind parameter for op() factory method."
            type BatchKind = Literal["user", "config", "service"]
            "Kind parameter for batch() factory method."
            type BatchPattern = Sequence[bool]
            "Pattern for batch result creation (True=success, False=failure)."
            type FactoryModel = BaseModel
            "Base type for all factory model types (Pydantic BaseModel)."

        class Files:
            """File-specific type definitions for test file operations (tf)."""

            type FormatLiteral = Literal[
                "auto",
                "text",
                "bin",
                "json",
                "yaml",
                "csv",
                "txt",
                "md",
            ]
            "Literal type for file format specification in create/read operations."
            type OperationLiteral = Literal[
                "create",
                "read",
                "delete",
                "compare",
                "info",
            ]
            "Literal type for batch operation specification."
            type ErrorModeLiteral = Literal["stop", "skip", "collect"]
            "Error handling mode for batch operations."
            type BatchFiles = (
                Mapping[str, t.Tests.Testobject] | Sequence[t.Tests.Testobject]
            )
            "Type for batch file operations - Mapping or Sequence of files."

        class Matcher:
            """Matcher-specific type definitions for test assertions (tm.* methods)."""

            type MatcherKwargValue = (
                _Testobject
                | type
                | tuple[type, ...]
                | TypeAliasType
                | set[_Testobject]
                | Callable[..., _Testobject]
                | Mapping[str, Callable[..., _Testobject] | _Testobject]
                | Mapping[int, Callable[..., _Testobject] | _Testobject]
            )
            "Type for matcher keyword argument values."
            type LengthSpec = int | tuple[int, int]
            "Length specification: exact int or (min, max) tuple."
            type DeepSpec = Mapping[
                str,
                Callable[[FlextTestsTypes.Tests.Testobject], bool]
                | FlextTestsTypes.Tests.Testobject,
            ]
            "Deep structural matching specification: path -> value or predicate."
            type PathSpec = str | Sequence[str]
            "Path specification for nested value extraction."
            type PredicateSpec = Callable[[FlextTestsTypes.Tests.Testobject], bool]
            "Predicate function for custom assertions."
            type ValueSpec = (
                Callable[[FlextTestsTypes.Tests.Testobject], bool]
                | FlextTestsTypes.Tests.Testobject
            )
            "Value specification: direct value or predicate function."
            type AssertionSpec = (
                Mapping[str, FlextTestsTypes.Tests.Testobject]
                | Callable[[FlextTestsTypes.Tests.Testobject], bool]
                | type
                | tuple[type, ...]
            )
            "Assertion specification for type/predicate/mapping checks."
            type ContainmentSpec = (
                FlextTestsTypes.Tests.Testobject
                | Sequence[FlextTestsTypes.Tests.Testobject]
            )
            "Containment specification: single item or sequence of items."
            type ExclusionSpec = str | Sequence[str]
            "Exclusion specification: single string or sequence of strings."
            type SequencePredicate = (
                type | Callable[[FlextTestsTypes.Tests.Testobject], bool]
            )
            "Sequence predicate for all/any matching."
            type SortKey = (
                bool
                | Callable[
                    [FlextTestsTypes.Tests.Testobject],
                    FlextTestsTypes.Tests.Testobject,
                ]
            )
            "Sort key specification: bool for natural sort or callable."
            type KeySpec = Sequence[str] | set[str]
            "Key specification: sequence or set of keys."
            type KeyValueSpec = (
                tuple[str, FlextTestsTypes.Tests.Testobject]
                | Mapping[str, FlextTestsTypes.Tests.Testobject]
            )
            "Key-value specification: single pair or mapping."
            type AttributeSpec = str | Sequence[str]
            "Attribute specification: single attribute or sequence."
            type AttributeValueSpec = (
                tuple[str, FlextTestsTypes.Tests.Testobject]
                | Mapping[str, FlextTestsTypes.Tests.Testobject]
            )
            "Attribute-value specification: single pair or mapping."
            type ErrorCodeSpec = str | Sequence[str]
            "Error code specification: single code or sequence."
            type ErrorDataSpec = m.ConfigMap
            "Error data specification: key-value pairs."
            type CleanupSpec = Sequence[Callable[[], None]]
            "Cleanup specification: sequence of cleanup functions."
            type EnvironmentSpec = Mapping[str, str]
            "Environment specification: mapping of env var names to values."

    class Guards:
        """TypeGuard functions for type narrowing."""

        @staticmethod
        def is_general_value(
            value: FlextTestsTypes.Tests.Testobject,
        ) -> TypeIs[FlextTestsTypes.Tests.Testobject]:
            """Check if value is payload-compatible."""
            if value is None:
                return True
            if isinstance(value, (str, int, float, bool, bytes)):
                return True
            if isinstance(value, BaseModel):
                return True
            return isinstance(value, (list, dict))


t = FlextTestsTypes

__all__ = ["FlextTestsTypes", "t"]
