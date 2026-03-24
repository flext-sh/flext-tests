"""Type system foundation for FLEXT tests.

Provides FlextTestsTypes, extending t with test-specific type definitions
for test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
import types as _bt
from collections.abc import (
    Callable,
    ItemsView,
    KeysView,
    Mapping,
    MutableMapping,
    Sequence,
    Set as AbstractSet,
    ValuesView,
)
from datetime import datetime
from enum import Enum
from pathlib import Path
from types import FrameType, GenericAlias, ModuleType
from typing import TypeAliasType, TypeIs

from flext_core import FlextResult, FlextTypes, p
from pydantic import BaseModel, InstanceOf, SecretStr

type _TestobjectSerializable = (
    FlextTypes.Primitives
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
    | BaseException
    | Exception
    | Enum
    | SecretStr
    | p.Logger
    | p.Container
    | p.Dispatcher
    | p.Settings
    | p.Context
    | FlextResult[_Testobject]
    | re.Match[str]
    | _bt.UnionType
    | FrameType
    | ModuleType
    | GenericAlias
    | set[_Testobject]
    | AbstractSet[_Testobject]
    | ValuesView[_Testobject]
    | KeysView[str]
    | ItemsView[str, _Testobject]
    | MutableMapping[str, _Testobject]
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

        All test-specific types organized under FlextTypes.Tests.* pattern.
        """

        type Testobject = _Testobject
        type TestobjectSerializable = _TestobjectSerializable
        type NormalizedValue = _Testobject
        type FileContent = (
            str
            | bytes
            | Mapping[str, _Testobject]
            | Sequence[FlextTypes.StrSequence]
            | InstanceOf[BaseModel]
        )
        type TestResultValue = _Testobject
        "Type for test result values."

        class Files:
            """File-specific type definitions for test file operations (tf)."""

            "File-specific types removed — use c.Tests.Files.Format, Operation, ErrorMode StrEnums."
            type BatchFiles = (
                Mapping[str, FlextTestsTypes.Tests.Testobject]
                | Sequence[FlextTestsTypes.Tests.Testobject]
            )
            "Type for batch file operations - Mapping or Sequence of files."

            type FileContentPlain = (
                str
                | bytes
                | FlextTypes.ConfigMap
                | Sequence[FlextTypes.StrSequence]
                | BaseModel
            )
            "Plain file content (no result wrapper): str, bytes, ConfigMap, CSV rows, or any Pydantic model."

            type FileInput = (
                FlextTestsTypes.Tests.Files.FileContentPlain
                | FlextResult[str]
                | FlextResult[bytes]
                | FlextResult[FlextTypes.ConfigMap]
                | FlextResult[Sequence[FlextTypes.StrSequence]]
                | FlextResult[BaseModel]
            )
            "Full file input type: plain content or result-wrapped content."

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
            type PathSpec = str | FlextTypes.StrSequence
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
            type ExclusionSpec = str | FlextTypes.StrSequence
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
            type KeySpec = FlextTypes.StrSequence | set[str]
            "Key specification: sequence or set of keys."
            type KeyValueSpec = (
                tuple[str, FlextTestsTypes.Tests.Testobject]
                | Mapping[str, FlextTestsTypes.Tests.Testobject]
            )
            "Key-value specification: single pair or mapping."
            type AttributeSpec = str | FlextTypes.StrSequence
            "Attribute specification: single attribute or sequence."
            type AttributeValueSpec = (
                tuple[str, FlextTestsTypes.Tests.Testobject]
                | Mapping[str, FlextTestsTypes.Tests.Testobject]
            )
            "Attribute-value specification: single pair or mapping."
            type ErrorCodeSpec = str | FlextTypes.StrSequence
            "Error code specification: single code or sequence."
            type ErrorDataSpec = FlextTypes.ConfigMap
            "Error data specification: key-value pairs."
            type CleanupSpec = Sequence[Callable[[], None]]
            "Cleanup specification: sequence of cleanup functions."
            type EnvironmentSpec = FlextTypes.StrMapping
            "Environment specification: mapping of env var names to values."

    class Guards:
        """TypeGuard functions for type narrowing.

        These guards use TypeIs to provide clean narrowing for recursive
        _Testobject types, avoiding pyright's partially-unknown type issues
        that occur when isinstance narrowing on unions containing Callable[...]
        or empty Protocol members (p.Base).
        """

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

        @staticmethod
        def is_testobject_mapping(
            value: FlextTestsTypes.Tests.Testobject
            | FlextTestsTypes.Tests.Matcher.MatcherKwargValue,
        ) -> TypeIs[Mapping[str, FlextTestsTypes.Tests.Testobject]]:
            """Narrow _Testobject to Mapping[str, _Testobject]."""
            return isinstance(value, Mapping)

        @staticmethod
        def is_testobject_set(
            value: FlextTestsTypes.Tests.Testobject
            | FlextTestsTypes.Tests.Matcher.MatcherKwargValue,
        ) -> TypeIs[set[FlextTestsTypes.Tests.Testobject] | frozenset[str]]:
            """Narrow _Testobject to set or frozenset."""
            return isinstance(value, (set, frozenset))

        @staticmethod
        def is_testobject_sequence(
            value: FlextTestsTypes.Tests.Testobject
            | FlextTestsTypes.Tests.Matcher.MatcherKwargValue,
        ) -> TypeIs[Sequence[FlextTestsTypes.Tests.Testobject]]:
            """Narrow _Testobject to non-string Sequence."""
            return isinstance(value, Sequence) and not isinstance(
                value,
                (str, bytes, bytearray),
            )

        @staticmethod
        def is_testobject_result(
            value: FlextTestsTypes.Tests.Testobject
            | FlextTestsTypes.Tests.Matcher.MatcherKwargValue,
        ) -> TypeIs[FlextResult[FlextTestsTypes.Tests.Testobject]]:
            """Narrow _Testobject to FlextResult."""
            return isinstance(value, FlextResult)


t = FlextTestsTypes

__all__ = ["FlextTestsTypes", "t"]
