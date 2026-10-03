"""Pytest case MRO surface for flext-tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import p

if TYPE_CHECKING:
    from flext_tests._settings import FlextTestsSettings
    from flext_tests.base import FlextTestsServiceBase


class FlextTestsCase:
    """Pytest class MRO surface populated by the shared test runtime fixture."""

    service: FlextTestsServiceBase[p.Base]
    settings: FlextTestsSettings
    logger: p.Logger
    c: type
    e: type
    m: type
    p: type
    r: type
    t: type
    u: type


__all__: list[str] = ["FlextTestsCase"]
