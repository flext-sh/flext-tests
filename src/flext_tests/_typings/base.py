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
from typing import Literal

from flext_cli import m, p, t

from flext_tests import c


class FlextTestsTypesBase:
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
    type PayloadItems[NodeT] = tuple[NodeT, ...]
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
        Sequence[FlextTestsTypesBase.TestobjectSerializable]
        | Mapping[str, FlextTestsTypesBase.TestobjectSerializable]
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
        | Sequence[TestobjectNode]
        | Mapping[str, TestobjectNode]
        | set[TestobjectHashable]
        | None
    )

    type TestResultValue = (
        FlextTestsTypesBase.TestobjectSerializable
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
        | p.Result[FlextTestsTypesBase.TestobjectSerializable]
        | t.RegexMatch
        | bt.UnionType
        | FrameType
        | ModuleType
        | GenericAlias
        | set[FlextTestsTypesBase.TestobjectHashable]
        | AbstractSet[FlextTestsTypesBase.TestobjectHashable]
        | ValuesView[FlextTestsTypesBase.TestobjectSerializable]
        | KeysView[str]
        | ItemsView[str, FlextTestsTypesBase.TestobjectSerializable]
        | MutableMapping[str, FlextTestsTypesBase.TestobjectSerializable]
        | tzinfo
        | timezone
    )
    "Type for FLEXT test result payloads."

    type Testobject = (
        FlextTestsTypesBase.TestResultValue
        | p.Result[FlextTestsTypesBase.TestResultValue]
    )


__all__: list[str] = ["FlextTestsTypesBase"]
