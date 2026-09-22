"""FLEXT Tests API facade — thin Railway-oriented MRO surface.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from .base import FlextTestsServiceBase


class FlextTests(FlextTestsServiceBase):
    """Railway-oriented api facade for flext-tests."""


api = FlextTests

__all__: tuple[str, ...] = ("FlextTests", "api")
