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
from flext_core import FlextModelsPydantic, p
from flext_tests import m

BaseModel = FlextModelsPydantic.BaseModel
ConfigDict = FlextModelsPydantic.ConfigDict
SecretStr = t.SecretStr
TypeAdapter = FlextModelsPydantic.TypeAdapter


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

    type TestResultValue = (
        FlextTestsBaseTypesMixin.TestobjectSerializable
        | t.RegisterableService
        | t.TypeHintSpecifier
        | BaseException
        | Exception
        | Enum
        | SecretStr
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

    TESTOBJECT_SEQUENCE_ADAPTER: m.TypeAdapter[
        Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = TypeAdapter(
        Sequence[TestobjectSerializable],
        config=ConfigDict(arbitrary_types_allowed=True),
    )
    TESTOBJECT_MAPPING_ADAPTER: m.TypeAdapter[
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = TypeAdapter(
        Mapping[str, TestobjectSerializable],
        config=ConfigDict(arbitrary_types_allowed=True),
    )
    STR_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[Sequence[t.StrMapping]] = TypeAdapter(
        Sequence[t.StrMapping]
    )
    TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER: m.TypeAdapter[
        Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = TypeAdapter(
        Mapping[str, TestobjectSerializable],
        config=ConfigDict(arbitrary_types_allowed=True),
    )
    TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER: m.TypeAdapter[
        Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = TypeAdapter(
        Sequence[TestobjectSerializable],
        config=ConfigDict(arbitrary_types_allowed=True),
    )
    PRIMITIVES_MAPPING_ADAPTER: m.TypeAdapter[Mapping[str, t.Primitives]] = TypeAdapter(
        Mapping[str, t.Primitives]
    )
    NORMALIZED_VALUE_ADAPTER: m.TypeAdapter[t.Container] = TypeAdapter(t.Container)
    DICT_ADAPTER: m.TypeAdapter[m.Dict] = TypeAdapter(m.Dict)
    SCALAR_MAPPING_ADAPTER: m.TypeAdapter[t.ScalarMapping] = TypeAdapter(
        t.ScalarMapping
    )
    CONTAINER_MAPPING_ADAPTER: m.TypeAdapter[Mapping[str, t.Container]] = TypeAdapter(
        Mapping[str, t.Container]
    )
    CONTAINER_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[
        Sequence[Mapping[str, t.Container]]
    ] = TypeAdapter(Sequence[Mapping[str, t.Container]])
    STR_MAPPING_ADAPTER: m.TypeAdapter[t.StrMapping] = TypeAdapter(t.StrMapping)
    STR_MAPPING_MAPPING_ADAPTER: m.TypeAdapter[Mapping[str, t.StrMapping]] = (
        TypeAdapter(Mapping[str, t.StrMapping])
    )
    INTEGER_SEQUENCE_ADAPTER: m.TypeAdapter[Sequence[int]] = TypeAdapter(Sequence[int])
    STR_SEQUENCE_MAPPING_ADAPTER: m.TypeAdapter[Mapping[str, t.StrSequence]] = (
        TypeAdapter(Mapping[str, t.StrSequence])
    )
