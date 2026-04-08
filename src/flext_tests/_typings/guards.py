"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TypeIs

from pydantic import BaseModel

from flext_core import FlextResult
from flext_tests import FlextTestsBaseTypesMixin


class FlextTestsGuardsTypesMixin:
    @staticmethod
    def is_general_value(
        value: FlextTestsBaseTypesMixin.Testobject,
    ) -> TypeIs[FlextTestsBaseTypesMixin.Testobject]:
        if value is None:
            return True
        if isinstance(value, (str, int, float, bool, bytes)):
            return True
        if isinstance(value, BaseModel):
            return True
        return isinstance(value, (list, dict))

    @staticmethod
    def is_testobject_mapping(
        value: FlextTestsBaseTypesMixin.Testobject,
    ) -> TypeIs[Mapping[str, FlextTestsBaseTypesMixin.TestobjectSerializable]]:
        return isinstance(value, Mapping)

    @staticmethod
    def is_testobject_set(
        value: FlextTestsBaseTypesMixin.Testobject,
    ) -> TypeIs[set[FlextTestsBaseTypesMixin.TestobjectSerializable] | frozenset[str]]:
        return isinstance(value, (set, frozenset))

    @staticmethod
    def is_testobject_sequence(
        value: FlextTestsBaseTypesMixin.Testobject,
    ) -> TypeIs[Sequence[FlextTestsBaseTypesMixin.TestobjectSerializable]]:
        return isinstance(value, Sequence) and not isinstance(
            value, (str, bytes, bytearray)
        )

    @staticmethod
    def is_testobject_result(
        value: FlextTestsBaseTypesMixin.Testobject,
    ) -> TypeIs[FlextResult[FlextTestsBaseTypesMixin.TestobjectSerializable]]:
        return isinstance(value, FlextResult)
