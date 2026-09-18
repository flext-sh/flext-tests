"""Base tests typing primitives.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import types as bt
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
from typing import TYPE_CHECKING, Literal

from flext_cli import t
from flext_infra import m, t as it

from flext_core import p

from .._models.domains import FlextTestsDomainModelsMixin

if TYPE_CHECKING:
    from collections.abc import Callable

    from .._models.base import FlextTestsBaseModelsMixin
    from .._protocols.payload import FlextTestsPayloadProtocolsMixin

type _NativeMatchValue = (
    FlextTestsBaseTypesMixin.PayloadAtom
    | p.Model
    | list[_NativeMatchValue]
    | dict[str, _NativeMatchValue]
    | None
)


class FlextTestsBaseTypesMixin:
    """Base generic primitives extending Flext core aliases."""

    type PayloadKind = Literal["atom", "list", "tuple", "set", "frozenset", "mapping"]
    type PayloadAtom = (
        str
        | int
        | float
        | bool
        | bytes
        | datetime
        | tzinfo
        | Path
        | type
        | BaseException
    )
    type PayloadItems[NodeT] = tuple[NodeT, ...]
    type PayloadEntries[NodeT] = Mapping[str, NodeT]

    type TestobjectAtom = (
        str
        | int
        | float
        | bool
        | bytes
        | datetime
        | tzinfo
        | Path
        | m.BaseModel
        | type
        | frozenset[str]
    )
    type TestobjectCollection = (
        t.SequenceOf[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    )
    type TestobjectNode = TestobjectAtom | t.JsonValue | None
    type TestobjectSerializable = (
        TestobjectAtom | t.JsonValue | list[TestobjectNode] | Mapping[str, TestobjectNode] | None
    )
    type NativeMatchValue = _NativeMatchValue
    type DeepSpec = Mapping[
        str,
        FlextTestsBaseModelsMixin.Payload
        | Callable[[FlextTestsPayloadProtocolsMixin.Payload], bool],
    ]
    type TestobjectHashable = (
        str | int | float | bool | bytes | datetime | tzinfo | Path | type | None
    )
    type NormalizationInput = (
        TestobjectAtom
        | t.SequenceOf[TestobjectNode]
        | t.MappingKV[str, TestobjectNode]
        | set[TestobjectHashable]
        | None
    )

    type HandlerCaseSpec = FlextTestsDomainModelsMixin.HandlerCaseSpec

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
        | p.AttributeProbe
        | p.Result[FlextTestsBaseTypesMixin.TestobjectSerializable]
        | it.Infra.RegexMatch
        | bt.UnionType
        | FrameType
        | ModuleType
        | GenericAlias
        | set[FlextTestsBaseTypesMixin.TestobjectHashable]
        | AbstractSet[FlextTestsBaseTypesMixin.TestobjectHashable]
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
        | p.Result[FlextTestsBaseTypesMixin.TestResultValue]
    )

    TESTOBJECT_SERIALIZABLE_ADAPTER: m.TypeAdapter[TestobjectSerializable] = (
        m.TypeAdapter(
            TestobjectSerializable, config=m.ConfigDict(arbitrary_types_allowed=True)
        )
    )

    TESTOBJECT_SEQUENCE_ADAPTER: m.TypeAdapter[
        t.SequenceOf[FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = m.TypeAdapter(
        t.SequenceOf[TestobjectSerializable],
        config=m.ConfigDict(arbitrary_types_allowed=True),
    )
    TESTOBJECT_MAPPING_ADAPTER: m.TypeAdapter[
        t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = m.TypeAdapter(
        t.MappingKV[str, TestobjectSerializable],
        config=m.ConfigDict(arbitrary_types_allowed=True),
    )
    STR_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[t.SequenceOf[t.StrMapping]] = (
        m.TypeAdapter(t.SequenceOf[t.StrMapping])
    )
    TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER: m.TypeAdapter[
        t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = m.TypeAdapter(
        t.MappingKV[str, TestobjectSerializable],
        config=m.ConfigDict(arbitrary_types_allowed=True),
    )
    TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER: m.TypeAdapter[
        t.SequenceOf[FlextTestsBaseTypesMixin.TestobjectSerializable]
    ] = m.TypeAdapter(
        t.SequenceOf[TestobjectSerializable],
        config=m.ConfigDict(arbitrary_types_allowed=True),
    )
    DICT_ADAPTER: m.TypeAdapter[m.Dict] = m.TypeAdapter(m.Dict)
    SCALAR_MAPPING_ADAPTER: m.TypeAdapter[t.ScalarMapping] = m.TypeAdapter(
        t.ScalarMapping
    )
    CONTAINER_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[t.SequenceOf[t.JsonMapping]] = (
        m.TypeAdapter(t.SequenceOf[t.JsonMapping])
    )
    STR_MAPPING_MAPPING_ADAPTER: m.TypeAdapter[t.MappingKV[str, t.StrMapping]] = (
        m.TypeAdapter(t.MappingKV[str, t.StrMapping])
    )
    INTEGER_SEQUENCE_ADAPTER: m.TypeAdapter[Sequence[int]] = m.TypeAdapter(
        Sequence[int]
    )
    STR_SEQUENCE_MAPPING_ADAPTER: m.TypeAdapter[t.MappingKV[str, t.StrSequence]] = (
        m.TypeAdapter(t.MappingKV[str, t.StrSequence])
    )
