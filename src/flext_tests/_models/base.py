"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextModels
from flext_tests import t


class FlextTestsBaseModelsMixin:
    class Entity(FlextModels.Entity):
        """Factory entity class for tests."""

        name: str = ""
        value: t.Tests.Testobject = None

    class Value(FlextModels.Value):
        """Factory value t.NormalizedValue class for tests."""

        data: str = ""
        count: int = 0
