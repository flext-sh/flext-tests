"""Scenario data: connectivity-marked tests that must be deselected.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from flext_tests import c


@pytest.mark.parametrize("marker", c.Tests.CONNECTIVITY_MARKERS)
def test_external(marker: str) -> None:
    """Fail loudly if collection runs a test whose capability is absent."""
    pytest.fail(f"test executed under the {marker} capability")
