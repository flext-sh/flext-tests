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

from flext_cli import t
from flext_core import FlextModelsContainers, FlextModelsPydantic, p


class FlextTestsBaseTypesMixin:
    """Base generic primitives extending Flext core aliases."""

    type TestobjectAtom = (
        str
        | int
        | float
        | bool
        | bytes
        | datetime
        | tzinfo
        | Path
        | FlextModelsPydantic.BaseModel
        | type
        | frozenset[str]
    )
    type TestobjectCollection = (
        Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type TestobjectSerializable = TestobjectAtom | TestobjectCollection | None

    type TestResultValue = (
        FlextTestsBaseTypesMixin.TestobjectSerializable
        | t.RegisterableService
        | t.TypeHintSpecifier
        | BaseException
        | Exception
        | Enum
        | t.SecretStr
        | p.Logger
        | p.Container
        | p.Dispatcher
        | p.Settings
        | p.Context
        | p.Registry
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
    "Type for FLEXT test result payloads."

    type Testobject = (
        FlextTestsBaseTypesMixin.TestResultValue
        | p.ResultLike[FlextTestsBaseTypesMixin.TestResultValue]
    )

    TESTOBJECT_SEQUENCE_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = FlextModelsPydantic.TypeAdapter(
        Sequence[TestobjectSerializable],
        config=FlextModelsPydantic.ConfigDict(arbitrary_types_allowed=True),
    )
    TESTOBJECT_MAPPING_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = FlextModelsPydantic.TypeAdapter(
        Mapping[str, TestobjectSerializable],
        config=FlextModelsPydantic.ConfigDict(arbitrary_types_allowed=True),
    )
    STR_MAPPING_SEQUENCE_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Sequence[t.StrMapping]
    ] = FlextModelsPydantic.TypeAdapter(Sequence[t.StrMapping])
    TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = FlextModelsPydantic.TypeAdapter(
        Mapping[str, TestobjectSerializable],
        config=FlextModelsPydantic.ConfigDict(arbitrary_types_allowed=True),
    )
    TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = FlextModelsPydantic.TypeAdapter(
        Sequence[TestobjectSerializable],
        config=FlextModelsPydantic.ConfigDict(arbitrary_types_allowed=True),
    )
    PRIMITIVES_MAPPING_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Mapping[str, t.Primitives]
    ] = FlextModelsPydantic.TypeAdapter(Mapping[str, t.Primitives])
    NORMALIZED_VALUE_ADAPTER: FlextModelsPydantic.TypeAdapter[t.JsonValue] = (
        FlextModelsPydantic.TypeAdapter(t.JsonValue)
    )
    DICT_ADAPTER: FlextModelsPydantic.TypeAdapter[FlextModelsContainers.Dict] = (
        FlextModelsPydantic.TypeAdapter(FlextModelsContainers.Dict)
    )
    SCALAR_MAPPING_ADAPTER: FlextModelsPydantic.TypeAdapter[t.ScalarMapping] = (
        FlextModelsPydantic.TypeAdapter(t.ScalarMapping)
    )
    CONTAINER_MAPPING_ADAPTER: FlextModelsPydantic.TypeAdapter[t.JsonMapping] = (
        FlextModelsPydantic.TypeAdapter(t.JsonMapping)
    )
    CONTAINER_MAPPING_SEQUENCE_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Sequence[t.JsonMapping]
    ] = FlextModelsPydantic.TypeAdapter(Sequence[t.JsonMapping])
    STR_MAPPING_ADAPTER: FlextModelsPydantic.TypeAdapter[t.StrMapping] = (
        FlextModelsPydantic.TypeAdapter(t.StrMapping)
    )
    STR_MAPPING_MAPPING_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Mapping[str, t.StrMapping]
    ] = FlextModelsPydantic.TypeAdapter(Mapping[str, t.StrMapping])
    INTEGER_SEQUENCE_ADAPTER: FlextModelsPydantic.TypeAdapter[Sequence[int]] = (
        FlextModelsPydantic.TypeAdapter(Sequence[int])
    )
    STR_SEQUENCE_MAPPING_ADAPTER: FlextModelsPydantic.TypeAdapter[
        Mapping[str, t.StrSequence]
    ] = FlextModelsPydantic.TypeAdapter(Mapping[str, t.StrSequence])
