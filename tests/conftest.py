"""Shared pytest configuration for the flext-tests test suite."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from flext_tests import FlextTestsDocker

if TYPE_CHECKING:
    from . import t

pytest_plugins: t.VariadicTuple[str] = ("pytester",)


@pytest.fixture
def docker_manager(tmp_path: Path) -> FlextTestsDocker:
    """Docker manager over the suite fixtures with a per-test state directory."""
    return FlextTestsDocker(
        repository_root=Path(__file__).parent / "fixtures",
        state_dir=tmp_path / "docker-state",
    )
