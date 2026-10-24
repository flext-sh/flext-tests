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
    Set as AbstractSet,
    ValuesView,
)
from datetime import datetime, timezone, tzinfo
from enum import Enum
from pathlib import Path
from types import FrameType, GenericAlias, ModuleType
from typing import Literal

from flext_cli import m, p, t

from flext_tests import c


class FlextTestsBaseTypesMixin:
    """Base generic primitives extending Flext core aliases."""

    type PayloadKind = Literal[
        "atom", c.Action.LIST, "tuple", "set", "frozenset", "mapping"
    ]
    type PayloadAtom = (
        t.InstanceOf[str]
        | t.InstanceOf[int]
        | t.InstanceOf[float]
        | t.InstanceOf[bool]
        | t.InstanceOf[bytes]
        | t.InstanceOf[datetime]
        | t.InstanceOf[tzinfo]
        | t.InstanceOf[Path]
        | t.InstanceOf[type]
        | t.InstanceOf[BaseException]
    )
    type PayloadItems[NodeT] = t.VariadicTuple[NodeT]
    type PayloadEntries[NodeT] = Mapping[str, NodeT]

    type TestobjectAtom = (
        str
        | int
        | float
        | bool
        | bytes
        | datetime
        | t.InstanceOf[tzinfo]
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
        TestobjectAtom
        | t.JsonValue
        | list[TestobjectNode]
        | Mapping[str, TestobjectNode]
        | None
    )
    type TestobjectHashable = (
        str
        | int
        | float
        | bool
        | bytes
        | datetime
        | t.InstanceOf[tzinfo]
        | Path
        | type
        | None
    )
    type NormalizationInput = (
        TestobjectAtom
        | t.SequenceOf[TestobjectNode]
        | t.MappingKV[str, TestobjectNode]
        | set[TestobjectHashable]
        | None
    )

    type TestResultValue = (
        FlextTestsBaseTypesMixin.TestobjectSerializable
        | p.RegisterableService
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
        | t.RegexMatch
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


__all__: list[str] = ["FlextTestsBaseTypesMixin"]
