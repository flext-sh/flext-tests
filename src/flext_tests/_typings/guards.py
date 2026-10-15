"""Types extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeIs

from flext_core import m

if TYPE_CHECKING:
    from flext_tests._typings.base import FlextTestsBaseTypesMixin


class FlextTestsGuardsTypesMixin:
    @staticmethod
    def general_value(
        value: FlextTestsBaseTypesMixin.Testobject,
    ) -> TypeIs[FlextTestsBaseTypesMixin.Testobject]:
        if value is None:
            return True
        if isinstance(value, (str, int, float, bool, bytes)):
            return True
        if isinstance(value, m.BaseModel):
            return True
        return isinstance(value, (list, dict))


__all__: list[str] = ["FlextTestsGuardsTypesMixin"]
