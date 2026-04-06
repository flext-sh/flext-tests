"""Type system foundation for FLEXT tests.

Provides FlextTestsTypes, extending t with test-specific type definitions
for test infrastructure.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)

from pydantic import BaseModel, ConfigDict, InstanceOf, TypeAdapter

from flext_cli import FlextCliTypes
from flext_core import FlextResult
from flext_tests._typings.base import FlextTestsBaseTypesMixin
from flext_tests._typings.files import FlextTestsFilesTypesMixin
from flext_tests._typings.guards import FlextTestsGuardsTypesMixin
from flext_tests._typings.matchers import FlextTestsMatchersTypesMixin


class FlextTestsTypes(FlextCliTypes):
    """Type system foundation for FLEXT tests - extends t.

    Architecture: Extends t with test-specific type aliases and definitions.
    All base types from t are available through inheritance.
    """

    class Tests(
        FlextTestsBaseTypesMixin,
        FlextTestsFilesTypesMixin,
        FlextTestsMatchersTypesMixin,
        FlextTestsGuardsTypesMixin,
    ):
        """Test-specific type definitions namespace.

        All test-specific types organized under FlextCliTypes.Tests.* pattern.
        """

        TESTOBJECT_SEQUENCE_ADAPTER: TypeAdapter[
            Sequence[FlextTestsBaseTypesMixin.Testobject]
        ] = TypeAdapter(
            Sequence[FlextTestsBaseTypesMixin.Testobject],
            config=ConfigDict(arbitrary_types_allowed=True),
        )
        TESTOBJECT_MAPPING_ADAPTER: TypeAdapter[
            Mapping[str, FlextTestsBaseTypesMixin.Testobject]
        ] = TypeAdapter(
            Mapping[str, FlextTestsBaseTypesMixin.Testobject],
            config=ConfigDict(arbitrary_types_allowed=True),
        )
        STR_MAPPING_SEQUENCE_ADAPTER: TypeAdapter[
            Sequence[FlextCliTypes.StrMapping]
        ] = TypeAdapter(Sequence[FlextCliTypes.StrMapping])
        TESTOBJECT_SERIALIZABLE_MAPPING_ADAPTER: TypeAdapter[
            Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]
        ] = TypeAdapter(
            Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable],
            config=ConfigDict(arbitrary_types_allowed=True),
        )
        TESTOBJECT_SERIALIZABLE_SEQUENCE_ADAPTER: TypeAdapter[
            Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]
        ] = TypeAdapter(
            Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable],
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
            | Mapping[str, FlextTestsBaseTypesMixin.Testobject]
            | Sequence[FlextCliTypes.StrSequence]
            | InstanceOf[BaseModel]
        )
        type FileContentPlain = FileContent
        type FileInput = (
            FileContentPlain
            | FlextResult[FlextTestsBaseTypesMixin.Testobject]
            | FlextResult[Sequence[FlextCliTypes.StrSequence]]
            | FlextResult[bytes]
            | FlextResult[str]
            | None
        )
        type BatchFiles = (
            Mapping[str, FlextTestsBaseTypesMixin.Testobject]
            | Sequence[tuple[str, FlextTestsBaseTypesMixin.Testobject]]
        )
        type TestResultValue = FlextTestsBaseTypesMixin.Testobject
        "Type for test result values."


t = FlextTestsTypes

__all__ = ["FlextTestsTypes", "t"]
