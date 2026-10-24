"""pytest public functions the test tier calls through ``u.Tests``.

flext-tests is the pytest plugin, so pytest is a layer-zero library of its
facade families (ADR-028, operator ruling 2026-10-24); a test module never
imports pytest and calls these members instead. Each member is the pytest
function itself, read from the class namespace.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest


class FlextTestsPytestUtilitiesMixin:
    """pytest functions published under ``u.Tests``."""

    approx = staticmethod(pytest.approx)
    fixture = staticmethod(pytest.fixture)
    importorskip = staticmethod(pytest.importorskip)
    main = staticmethod(pytest.main)
    param = staticmethod(pytest.param)
    raises = staticmethod(pytest.raises)
    warns = staticmethod(pytest.warns)


__all__: list[str] = ["FlextTestsPytestUtilitiesMixin"]
