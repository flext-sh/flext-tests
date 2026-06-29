"""Unit tests for simplified flext_tests.docker module.

Tests essential Docker container management functionality:
- Container status/info retrieval
- Dirty state tracking
- Docker-compose operations
- Port readiness checking

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest

from tests import tk
from tests.unit._docker_parts.builders import DockerBuildersMixin
from tests.unit._docker_parts.operations import DockerOperationsMixin
from tests.unit._docker_parts.state import DockerStateMixin
from tests.unit._docker_parts.targets import DockerTargetsMixin


@pytest.fixture
def docker_manager(tmp_path: Path) -> tk:
    """Create a tk instance for testing."""
    fixtures_dir = Path(__file__).parent.parent.parent / "fixtures"
    manager = tk(workspace_root=fixtures_dir, worker_id=f"test-{tmp_path.name}")
    _ = manager.mark_container_clean("container1")
    _ = manager.mark_container_clean("container2")
    _ = manager.mark_container_clean("test_container")
    _ = manager.mark_container_clean("dirty_container")
    return manager


class TestsFlextTestsDocker(
    DockerStateMixin,
    DockerBuildersMixin,
    DockerTargetsMixin,
    DockerOperationsMixin,
):
    """Test suite for c.Tests.ContainerStatus enum."""
