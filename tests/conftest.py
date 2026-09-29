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
    """Create a Docker manager from the suite fixtures with clean containers."""
    manager = FlextTestsDocker(
        repository_root=Path(__file__).parent / "fixtures",
        worker_id=f"test-{tmp_path.name}",
    )
    _ = manager.mark_container_clean("container1")
    _ = manager.mark_container_clean("container2")
    _ = manager.mark_container_clean("test_container")
    _ = manager.mark_container_clean("dirty_container")
    return manager
