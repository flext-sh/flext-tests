"""Shared pytest configuration for the flext-tests test suite.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker
from tests import u

pytest_plugins: tuple[str, ...] = ("pytester",)


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Compose the live catalog outside per-item budgets for the dispatcher suite.

    The catalog owns one repository scan. Resolving it lazily inside the first
    dispatcher test charges that session-scoped scan to the item's slow budget,
    which fails under host contention although the test itself is small;
    collection is the owner of process-scoped resolution.
    """
    if any(
        item.path.stem == "test_enforcement_dispatcher"
        for item in items
        if isinstance(item, pytest.Function)
    ):
        u.Tests.build_canonical_catalog(Path(__file__).resolve().parents[1])


@pytest.fixture
def docker_manager(tmp_path: Path) -> FlextTestsDocker:
    """Docker manager over the suite fixtures with a per-test state directory.

    Returns:
        The resulting ``FlextTestsDocker``.

    """
    return FlextTestsDocker(
        repository_root=Path(__file__).parent / "fixtures",
        state_dir=tmp_path / "docker-state",
    )
