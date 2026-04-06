"""Protocols extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol


class FlextTestsValueFactoryProtocolsMixin:
    class ValueFactory[TValue](Protocol):
        """Factory protocol that builds value objects for test helpers.

        Methods:
            __call__: build a typed value instance given data and count.

        """

        def __call__(self, *, data: str, count: int) -> TValue:
            """Build a typed value instance."""
            ...
