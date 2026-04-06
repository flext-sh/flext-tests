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
    ItemsView,
    KeysView,
    Mapping,
    MutableMapping,
    Sequence,
    Set as AbstractSet,
    ValuesView,
)
from datetime import datetime, timezone, tzinfo
from enum import Enum
from pathlib import Path
from types import FrameType, GenericAlias, ModuleType

from pydantic import BaseModel, ConfigDict, InstanceOf, SecretStr, TypeAdapter

from flext_cli import FlextCliTypes
from flext_core import FlextResult, p


class FlextTestsTypes(FlextCliTypes):
    """Type system foundation for FLEXT tests - extends t.

    Architecture: Extends t with test-specific type aliases and definitions.
    All base types from t are available through inheritance.
    """

    class Tests:
        """Test-specific type definitions namespace.

        All test-specific types organized under FlextCliTypes.Tests.* pattern.
        """

        type TestobjectSerializable = (
            FlextCliTypes.Primitives
            | None
            | bytes
            | datetime
            | tzinfo
            | Path
            | BaseModel
            | type
            | frozenset[str]
            | Sequence[FlextTestsTypes.Tests.TestobjectSerializable]
            | Mapping[str, FlextTestsTypes.Tests.TestobjectSerializable]
        )

        type Testobject = (
            FlextTestsTypes.Tests.TestobjectSerializable
            | BaseException
            | Exception
            | Enum
            | SecretStr
            | p.Logger
            | p.Container
            | p.Dispatcher
            | p.Settings
            | p.Context
            | FlextResult[FlextTestsTypes.Tests.Testobject]
            | re.Match[str]
            | _bt.UnionType
            | FrameType
            | ModuleType
            | GenericAlias
            | set[FlextTestsTypes.Tests.Testobject]
            | AbstractSet[FlextTestsTypes.Tests.Testobject]
            | ValuesView[FlextTestsTypes.Tests.Testobject]
            | KeysView[str]
            | ItemsView[str, FlextTestsTypes.Tests.Testobject]
            | MutableMapping[str, FlextTestsTypes.Tests.Testobject]
            | Sequence[FlextTestsTypes.Tests.Testobject]
            | Mapping[str, FlextTestsTypes.Tests.Testobject]
            | tzinfo
            | timezone
        )

        TESTOBJECT_SEQUENCE_ADAPTER: TypeAdapter[Sequence[Testobject]] = TypeAdapter(
            Sequence[Testobject],
            config=ConfigDict(arbitrary_types_allowed=True),
        )
        TESTOBJECT_MAPPING_ADAPTER: TypeAdapter[Mapping[str, Testobject]] = TypeAdapter(
            Mapping[str, Testobject],
            config=ConfigDict(arbitrary_types_allowed=True),
        )
        STR_MAPPING_SEQUENCE_ADAPTER: TypeAdapter[
            Sequence[FlextCliTypes.StrMapping]
        ] = TypeAdapter(Sequence[FlextCliTypes.StrMapping])
        TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER: TypeAdapter[
            Mapping[str, TestobjectSerializable]
        ] = TypeAdapter(
            Mapping[str, TestobjectSerializable],
            config=ConfigDict(arbitrary_types_allowed=True),
        )
        TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER: TypeAdapter[
            Sequence[TestobjectSerializable]
        ] = TypeAdapter(
            Sequence[TestobjectSerializable],
            config=ConfigDict(arbitrary_types_allowed=True),
        )
        PRIMITIVES_MAPPING_ADAPTER: TypeAdapter[
            Mapping[str, FlextCliTypes.Primitives]
        ] = TypeAdapter(Mapping[str, FlextCliTypes.Primitives])
        NORMALIZED_VALUE_ADAPTER: TypeAdapter[FlextCliTypes.NormalizedValue] = (
            TypeAdapter(FlextCliTypes.NormalizedValue)
        )
        DICT_ADAPTER: TypeAdapter[FlextCliTypes.Dict] = TypeAdapter(FlextCliTypes.Dict)
        SCALAR_MAPPING_ADAPTER: TypeAdapter[FlextCliTypes.ScalarMapping] = TypeAdapter(
            FlextCliTypes.ScalarMapping
        )
        CONTAINER_MAPPING_ADAPTER: TypeAdapter[FlextCliTypes.ContainerMapping] = (
            TypeAdapter(FlextCliTypes.ContainerMapping)
        )
        CONTAINER_MAPPING_SEQUENCE_ADAPTER: TypeAdapter[
            Sequence[FlextCliTypes.ContainerMapping]
        ] = TypeAdapter(Sequence[FlextCliTypes.ContainerMapping])
        STR_MAPPING_ADAPTER: TypeAdapter[FlextCliTypes.StrMapping] = TypeAdapter(
            FlextCliTypes.StrMapping
        )
        STR_MAPPING_MAPPING_ADAPTER: TypeAdapter[
            Mapping[str, FlextCliTypes.StrMapping]
        ] = TypeAdapter(Mapping[str, FlextCliTypes.StrMapping])
        INTEGER_SEQUENCE_ADAPTER: TypeAdapter[Sequence[int]] = TypeAdapter(
            Sequence[int]
        )
        STR_SEQUENCE_MAPPING_ADAPTER: TypeAdapter[
            Mapping[str, FlextCliTypes.StrSequence]
        ] = TypeAdapter(Mapping[str, FlextCliTypes.StrSequence])

        type FileContent = (
            str
            | bytes
            | Mapping[str, Testobject]
            | Sequence[FlextCliTypes.StrSequence]
            | InstanceOf[BaseModel]
        )
        type TestResultValue = Testobject
        "Type for test result values."

        class Files:
            """File-specific type definitions for test file operations (tf)."""
