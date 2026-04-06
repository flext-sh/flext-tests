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

from pydantic import BaseModel, SecretStr

from flext_core import FlextResult, FlextTypes, p


class FlextTestsBaseTypesMixin:
    """Base generic primitives extending Flext core aliases."""

    type TestobjectSerializable = (
        FlextTypes.Primitives
        | bytes
        | datetime
        | tzinfo
        | Path
        | BaseModel
        | type
        | frozenset[str]
        | Sequence[TestobjectSerializable]
        | Mapping[str, TestobjectSerializable]
        | None
    )

    type Testobject = (
        TestobjectSerializable
        | BaseException
        | Exception
        | Enum
        | SecretStr
        | p.Logger
        | p.Container
        | p.Dispatcher
        | p.Settings
        | p.Context
        | FlextResult[FlextTestsBaseTypesMixin.Testobject]
        | re.Match[str]
        | _bt.UnionType
        | FrameType
        | ModuleType
        | GenericAlias
        | set[Testobject]
        | AbstractSet[Testobject]
        | ValuesView[Testobject]
        | KeysView[str]
        | ItemsView[str, Testobject]
        | MutableMapping[str, Testobject]
        | Sequence[Testobject]
        | Mapping[str, Testobject]
        | tzinfo
        | timezone
    )
