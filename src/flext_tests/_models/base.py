"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_core import FlextModels
from flext_tests import t


class FlextTestsBaseModelsMixin:
    class Entity(FlextModels.Entity):
        """Factory entity class for tests."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        name: Annotated[str, FlextModels.Field(description="Entity display name.")] = ""
        value: Annotated[
            t.Tests.TestobjectSerializable,
            FlextModels.Field(description="Arbitrary serializable payload."),
        ] = None

    class Value(FlextModels.Value):
        """Factory value object class for tests."""

        data: Annotated[str, FlextModels.Field(description="Payload data string.")] = ""
        count: Annotated[int, FlextModels.Field(description="Occurrence counter.")] = 0
