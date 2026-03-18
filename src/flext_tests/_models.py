"""Auto-generated centralized models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, ConfigDict, RootModel, TypeAdapter


class FlextAutoConstants:
    pass


class FlextAutoTypes:
    class Tests:
        Testobject: type[BaseModel]


class FlextAutoProtocols:
    pass


class FlextAutoUtilities:
    pass


class FlextAutoModels:
    pass


c = FlextAutoConstants
t = FlextAutoTypes
p = FlextAutoProtocols
u = FlextAutoUtilities
m = FlextAutoModels


_ARBTYPES = ConfigDict(arbitrary_types_allowed=True)


class _TestObject(
    RootModel[
        str
        | int
        | float
        | bool
        | None
        | bytes
        | datetime
        | Path
        | BaseModel
        | type
        | frozenset[str]
        | Sequence["_TestObject"]
        | Mapping[str, "_TestObject"]
    ],
):
    pass


FlextAutoTypes.Tests.Testobject = _TestObject


class _TestContainerDictAdapter(RootModel[TypeAdapter(dict[str, t.Tests.Testobject])]):
    pass


class _ObjectDictAdapter(RootModel[TypeAdapter(dict[str, t.Tests.Testobject])]):
    pass


class _TestPayloadDictAdapter(RootModel[TypeAdapter(dict[str, t.Tests.Testobject])]):
    pass


class _GuardPayloadDictAdapter(RootModel[TypeAdapter(dict[str, t.Tests.Testobject])]):
    pass


class _PayloadMappingAdapter(
    RootModel[TypeAdapter(dict[str, t.Tests.Testobject], config=_ARBTYPES)],
):
    pass
