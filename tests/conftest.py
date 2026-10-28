"""Shared pytest configuration for the flext-tests test suite.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker

pytest_plugins: tuple[str, ...] = ("pytester",)


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
