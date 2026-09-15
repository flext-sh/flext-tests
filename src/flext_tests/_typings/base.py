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
from typing import NotRequired, TypedDict

from flext_cli import t
from flext_infra import t as it

from flext_core import m, p

# Module-level recursive type aliases (forward references work with from __future__ import annotations)
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

type TestobjectSerializable = (
    TestobjectAtom
    | list[TestobjectSerializable]
    | Mapping[str, TestobjectSerializable]
    | None
)

type TestobjectHashable = (
    str | int | float | bool | bytes | datetime | tzinfo | Path | type | None
)

type NormalizationInput = (
    TestobjectAtom
    | Sequence[NormalizationInput]
    | Mapping[str, NormalizationInput]
    | set[TestobjectHashable]
    | None
)


class FlextTestsBaseTypesMixin:
    """Base generic primitives extending Flext core aliases."""

    # Re-export module-level types as class attributes for backward compatibility
    TestobjectAtom = TestobjectAtom
    TestobjectSerializable = TestobjectSerializable
    TestobjectHashable = TestobjectHashable
    NormalizationInput = NormalizationInput

    type TestobjectCollection = (
        t.SequenceOf[TestobjectSerializable] | t.MappingKV[str, TestobjectSerializable]
    )

    class HandlerCaseSpec(TypedDict):
        handler_id: str
        handler_type: str
        description: str
        expected_result: NotRequired[str]
        should_fail: NotRequired[bool]
        error_message: NotRequired[str]

    type TestResultValue = (
        TestobjectSerializable
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
        | p.Result[TestobjectSerializable]
        | it.Infra.RegexMatch
        | bt.UnionType
        | FrameType
        | ModuleType
        | GenericAlias
        | set[TestobjectHashable]
        | AbstractSet[TestobjectHashable]
        | ValuesView[TestobjectSerializable]
        | KeysView[str]
        | ItemsView[str, TestobjectSerializable]
        | MutableMapping[str, TestobjectSerializable]
        | tzinfo
        | timezone
    )
    "Type for FLEXT test result payloads."

    type Testobject = TestResultValue | p.Result[TestResultValue]

    TESTOBJECT_SERIALIZABLE_ADAPTER: m.TypeAdapter[TestobjectSerializable] = (
        m.TypeAdapter(
            TestobjectSerializable, config=m.ConfigDict(arbitrary_types_allowed=True)
        )
    )

    TESTOBJECT_SEQUENCE_ADAPTER: m.TypeAdapter[t.SequenceOf[TestobjectSerializable]] = (
        m.TypeAdapter(
            t.SequenceOf[TestobjectSerializable],
            config=m.ConfigDict(arbitrary_types_allowed=True),
        )
    )
    TESTOBJECT_MAPPING_ADAPTER: m.TypeAdapter[
        t.MappingKV[str, TestobjectSerializable]
    ] = m.TypeAdapter(
        t.MappingKV[str, TestobjectSerializable],
        config=m.ConfigDict(arbitrary_types_allowed=True),
    )
    STR_MAPPING_SEQUENCE_ADAPTER: m.TypeAdapter[t.SequenceOf[t.StrMapping]] = (
        m.TypeAdapter(t.SequenceOf[t.StrMapping])
    )
    TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER: m.TypeAdapter[
        t.MappingKV[str, TestobjectSerializable]
    ] = m.TypeAdapter(
        t.MappingKV[str, TestobjectSerializable],
        config=m.ConfigDict(arbitrary_types_allowed=True),
    )
    TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER: m.TypeAdapter[
        t.SequenceOf[TestobjectSerializable]
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
