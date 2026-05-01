"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from tests import t

from flext_core import m


class FlextTestsBaseModelsMixin:
    class Entity(m.Entity):
        """Factory entity class for tests."""

        name: Annotated[str, m.Field(description="Entity display name.")] = ""
        value: Annotated[
            t.Tests.TestobjectSerializable,
            m.Field(description="Arbitrary serializable payload."),
        ] = None

    class Value(m.Value):
        """Factory value object class for tests."""

        data: Annotated[str, m.Field(description="Payload data string.")] = ""
        count: Annotated[int, m.Field(description="Occurrence counter.")] = 0
