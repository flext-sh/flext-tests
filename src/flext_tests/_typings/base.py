"""Base tests typing primitives.

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

from pydantic import BaseModel, ConfigDict, SecretStr, TypeAdapter

from flext_cli import t
from flext_core import FlextResult, p


class FlextTestsBaseTypesMixin:
    """Base generic primitives extending Flext core aliases."""

    type TestobjectSerializable = (
        str
        | int
        | float
        | bool
        | bytes
        | datetime
        | tzinfo
        | Path
        | BaseModel
        | type
        | frozenset[str]
        | Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | None
    )

    type Testobject = (
        FlextTestsBaseTypesMixin.TestobjectSerializable
        | BaseException
        | Exception
        | Enum
        | SecretStr
        | p.Logger
        | p.Container
        | p.Dispatcher
        | p.Settings
        | p.Context
        | FlextResult[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | re.Match[str]
        | _bt.UnionType
        | FrameType
        | ModuleType
        | GenericAlias
        | set[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | AbstractSet[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | ValuesView[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | KeysView[str]
        | ItemsView[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | MutableMapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        | tzinfo
        | timezone
    )

    TESTOBJECT_SEQUENCE_ADAPTER: TypeAdapter[
        Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    ]
    TESTOBJECT_MAPPING_ADAPTER: TypeAdapter[
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    ]
    STR_MAPPING_SEQUENCE_ADAPTER: TypeAdapter[Sequence[t.StrMapping]] = TypeAdapter(
        Sequence[t.StrMapping]
    )
    TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER: TypeAdapter[
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    ]
    TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER: TypeAdapter[
        Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    ]
    PRIMITIVES_MAPPING_ADAPTER: TypeAdapter[Mapping[str, t.Primitives]] = TypeAdapter(
        Mapping[str, t.Primitives]
    )
    NORMALIZED_VALUE_ADAPTER: TypeAdapter[t.NormalizedValue] = TypeAdapter(
        t.NormalizedValue
    )
    DICT_ADAPTER: TypeAdapter[t.Dict] = TypeAdapter(t.Dict)
    SCALAR_MAPPING_ADAPTER: TypeAdapter[t.ScalarMapping] = TypeAdapter(t.ScalarMapping)
    CONTAINER_MAPPING_ADAPTER: TypeAdapter[t.ContainerMapping] = TypeAdapter(
        t.ContainerMapping
    )
    CONTAINER_MAPPING_SEQUENCE_ADAPTER: TypeAdapter[Sequence[t.ContainerMapping]] = (
        TypeAdapter(Sequence[t.ContainerMapping])
    )
    STR_MAPPING_ADAPTER: TypeAdapter[t.StrMapping] = TypeAdapter(t.StrMapping)
    STR_MAPPING_MAPPING_ADAPTER: TypeAdapter[Mapping[str, t.StrMapping]] = TypeAdapter(
        Mapping[str, t.StrMapping]
    )
    INTEGER_SEQUENCE_ADAPTER: TypeAdapter[Sequence[int]] = TypeAdapter(Sequence[int])
    STR_SEQUENCE_MAPPING_ADAPTER: TypeAdapter[Mapping[str, t.StrSequence]] = (
        TypeAdapter(Mapping[str, t.StrSequence])
    )

    type TestResultValue = FlextTestsBaseTypesMixin.Testobject
    "Type for test result values."


FlextTestsBaseTypesMixin.TESTOBJECT_SEQUENCE_ADAPTER = TypeAdapter(
    Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable],
    config=ConfigDict(arbitrary_types_allowed=True),
)
FlextTestsBaseTypesMixin.TESTOBJECT_MAPPING_ADAPTER = TypeAdapter(
    Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable],
    config=ConfigDict(arbitrary_types_allowed=True),
)
FlextTestsBaseTypesMixin.TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER = TypeAdapter(
    Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable],
    config=ConfigDict(arbitrary_types_allowed=True),
)
FlextTestsBaseTypesMixin.TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER = TypeAdapter(
    Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable],
    config=ConfigDict(arbitrary_types_allowed=True),
)
