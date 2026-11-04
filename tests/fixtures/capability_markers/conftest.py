"""Scenario data: marks external tests from their parametrized marker.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Attach the parametrized capability marker and the service fixture."""
    for item in items:
        if "test_external" in item.name:
            callspec = getattr(item, "callspec", None)
            if callspec is None:
                continue
            item.add_marker(getattr(pytest.mark, callspec.params["marker"]))
            item.add_marker(pytest.mark.usefixtures("service"))


@pytest.fixture
def service() -> None:
    """Fail loudly: a deselected capability test must never reach its service."""
    pytest.fail("service fixture executed")
