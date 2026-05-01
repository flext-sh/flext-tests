"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from typing import TypeIs

from flext_core import m, p
from flext_tests import t


class FlextTestsGuardsTypesMixin:
    @staticmethod
    def general_value(
        value: t.Tests.Testobject,
    ) -> TypeIs[t.Tests.Testobject]:
        if value is None:
            return True
        if isinstance(value, (str, int, float, bool, bytes)):
            return True
        if isinstance(value, m.BaseModel):
            return True
        return isinstance(value, (list, dict))

    @staticmethod
    def testobject_mapping(
        value: t.Tests.Testobject,
    ) -> TypeIs[Mapping[str, t.Tests.TestobjectSerializable]]:
        return isinstance(value, Mapping)

    @staticmethod
    def testobject_set(
        value: t.Tests.Testobject,
    ) -> TypeIs[set[t.Tests.TestobjectSerializable] | frozenset[str]]:
        return isinstance(value, (set, frozenset))

    @staticmethod
    def testobject_sequence(
        value: t.Tests.Testobject,
    ) -> TypeIs[Sequence[t.Tests.TestobjectSerializable]]:
        return isinstance(value, Sequence) and not isinstance(
            value, (str, bytes, bytearray)
        )

    @staticmethod
    def testobject_result(
        value: t.Tests.Testobject,
    ) -> TypeIs[p.ResultLike[t.Tests.TestResultValue]]:
        return isinstance(value, p.ResultLike)
