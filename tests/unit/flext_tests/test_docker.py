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

import json
import tempfile
from pathlib import Path

import pytest
from docker import DockerClient
from flext_core import r

from flext_tests import tm
from tests import c
from tests.test_utils import assertion_helpers


class TestContainerStatus:
    """Test suite for c.Tests.Docker.ContainerStatus enum."""

    def test_container_status_values(self) -> None:
        """Test c.Tests.Docker.ContainerStatus enum values."""
        tm.that(c.Tests.Docker.ContainerStatus.RUNNING.value == "running", eq=True)
        tm.that(c.Tests.Docker.ContainerStatus.STOPPED.value == "stopped", eq=True)
        tm.that(c.Tests.Docker.ContainerStatus.NOT_FOUND.value == "not_found", eq=True)
        tm.that(c.Tests.Docker.ContainerStatus.ERROR.value == "error", eq=True)


class TestContainerInfo:
    """Test suite for tk.ContainerInfo model."""

    def test_container_info_creation(self) -> None:
        """Test tk.ContainerInfo creation with required fields."""
        info = tk.ContainerInfo(
            name="test_container",
            status=c.Tests.Docker.ContainerStatus.RUNNING,
            ports={"8080/tcp": "8080"},
            image="nginx:latest",
        )
        tm.that(info.name == "test_container", eq=True)
        tm.that(info.status == c.Tests.Docker.ContainerStatus.RUNNING.value, eq=True)
        tm.that(info.ports == {"8080/tcp": "8080"}, eq=True)
        tm.that(info.image == "nginx:latest", eq=True)
        tm.that(not info.container_id, eq=True)

    def test_container_info_with_container_id(self) -> None:
        """Test tk.ContainerInfo with container_id."""
        info = tk.ContainerInfo(
            name="test_container",
            status=c.Tests.Docker.ContainerStatus.RUNNING,
            ports={},
            image="nginx:latest",
            container_id="abc123",
        )
        tm.that(info.container_id == "abc123", eq=True)


class TestFlextTestsDocker:
    """Test suite for tk class."""

    @pytest.fixture
    def docker_manager(self, tmp_path: Path) -> tk:
        """Create a tk instance for testing."""
        fixtures_dir = Path(__file__).parent.parent.parent / "fixtures"
        manager = tk(workspace_root=fixtures_dir)
        manager._state_file = tmp_path / "test_docker_state.json"
        manager._dirty_containers.clear()
        return manager

    def test_init(self, docker_manager: tk) -> None:
        """Test tk initialization."""
        tm.that(isinstance(docker_manager, tk), eq=True)
        tm.that(docker_manager.workspace_root is not None, eq=True)
        tm.that(isinstance(docker_manager._dirty_containers, set), eq=True)

    def test_get_client_initialization(self) -> None:
        """Test Docker client lazy initialization."""
        manager = tk()
        manager._dirty_containers.clear()
        manager._client = None
        client = manager.get_client()
        tm.that(client is not None, eq=True)
        tm.that(manager._client is not None, eq=True)
        tm.that(isinstance(client, DockerClient), eq=True)

    def test_get_client_cached(self) -> None:
        """Test Docker client caching."""
        manager = tk()
        manager._dirty_containers.clear()
        manager._client = None
        client1 = manager.get_client()
        client2 = manager.get_client()
        tm.that(client1 is client2, eq=True)

    def test_load_dirty_state_file_not_exists(
        self,
        docker_manager: tk,
    ) -> None:
        """Test loading dirty state when file doesn't exist."""
        docker_manager._state_file = Path("/tmp/nonexistent_state.json")
        docker_manager._load_dirty_state()
        tm.that(docker_manager._dirty_containers == set(), eq=True)

    def test_load_dirty_state_file_exists(
        self,
        docker_manager: tk,
    ) -> None:
        """Test loading dirty state from existing file."""
        test_data = {"dirty_containers": ["container1", "container2"]}
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            delete=False,
            suffix=".json",
        ) as f:
            json.dump(test_data, f)
            temp_file = Path(f.name)
        try:
            docker_manager._state_file = temp_file
            docker_manager._load_dirty_state()
            tm.that("container1" in docker_manager._dirty_containers, eq=True)
            tm.that("container2" in docker_manager._dirty_containers, eq=True)
        finally:
            temp_file.unlink()

    def test_save_dirty_state(
        self,
        docker_manager: tk,
        tmp_path: Path,
    ) -> None:
        """Test saving dirty state to file.

        Validates:
        1. Dirty state is saved to file correctly
        2. File is created in tmp_path (not permanent location)
        3. Saved data matches expected content
        4. File can be read back correctly
        """
        docker_manager._dirty_containers = {"test_container"}
        tm.that(docker_manager._state_file.parent == tmp_path, eq=True)
        tm.that(docker_manager._state_file.name == "test_docker_state.json", eq=True)
        docker_manager._save_dirty_state()
        tm.that(docker_manager._state_file.exists(), eq=True)
        with docker_manager._state_file.open("r") as f:
            data = json.load(f)
        tm.that("dirty_containers" in data, eq=True)
        tm.that(isinstance(data["dirty_containers"], list), eq=True)
        tm.that("test_container" in data["dirty_containers"], eq=True)
        tm.that(len(data["dirty_containers"]) == 1, eq=True)

    def test_mark_container_dirty(self, docker_manager: tk) -> None:
        """Test marking container as dirty."""
        result = docker_manager.mark_container_dirty("test_container")
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that("test_container" in docker_manager._dirty_containers, eq=True)

    def test_mark_container_clean(self, docker_manager: tk) -> None:
        """Test marking container as clean."""
        docker_manager._dirty_containers.add("test_container")
        result = docker_manager.mark_container_clean("test_container")
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that("test_container" not in docker_manager._dirty_containers, eq=True)

    def test_is_container_dirty(self, docker_manager: tk) -> None:
        """Test checking if container is dirty."""
        docker_manager._dirty_containers.add("dirty_container")
        tm.that(docker_manager.is_container_dirty("dirty_container"), eq=True)
        tm.that(not docker_manager.is_container_dirty("clean_container"), eq=True)

    def test_get_dirty_containers(self, docker_manager: tk) -> None:
        """Test getting list of dirty containers."""
        docker_manager._dirty_containers = {"container1", "container2"}
        dirty = docker_manager.get_dirty_containers()
        tm.that(len(dirty) == 2, eq=True)
        tm.that("container1" in dirty, eq=True)
        tm.that("container2" in dirty, eq=True)

    def test_shared_containers_attribute(self) -> None:
        """Test SHARED_CONTAINERS class attribute."""
        tm.that(tk.SHARED_CONTAINERS is not None, eq=True)
        tm.that(isinstance(tk.SHARED_CONTAINERS, dict), eq=True)

    def test_shared_containers_property(self, docker_manager: tk) -> None:
        """Test shared_containers property."""
        containers = docker_manager.shared_containers
        tm.that(containers is not None, eq=True)
        tm.that(isinstance(containers, dict), eq=True)

    def test_compose_up_returns_flext_result(
        self,
        docker_manager: tk,
    ) -> None:
        """Test compose_up returns r."""
        result = docker_manager.compose_up("docker-compose.yml")
        tm.that(isinstance(result, r), eq=True)

    def test_compose_down_returns_flext_result(
        self,
        docker_manager: tk,
    ) -> None:
        """Test compose_down returns r."""
        result = docker_manager.compose_down("docker-compose.yml")
        tm.that(isinstance(result, r), eq=True)

    def test_start_existing_container_not_found(
        self,
        docker_manager: tk,
    ) -> None:
        """Test starting non-existent container."""
        result = docker_manager.start_existing_container("nonexistent_container")
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("not found" in str(result.error).lower(), eq=True)

    def test_get_container_info_not_found(
        self,
        docker_manager: tk,
    ) -> None:
        """Test getting info for non-existent container."""
        result = docker_manager.get_container_info("nonexistent_container")
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("not found" in str(result.error).lower(), eq=True)

    def test_get_container_status_alias(self, docker_manager: tk) -> None:
        """Test get_container_status is alias for get_container_info."""
        result = docker_manager.get_container_status("nonexistent")
        _ = assertion_helpers.assert_flext_result_failure(result)

    def test_wait_for_port_ready_immediate(
        self,
        docker_manager: tk,
    ) -> None:
        """Test wait_for_port_ready returns quickly for unavailable port."""
        result = docker_manager.wait_for_port_ready(
            c.Network.LOOPBACK_IP,
            59999,
            max_wait=1,
        )
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value is False, eq=True)

    def test_start_compose_stack_returns_result(
        self,
        docker_manager: tk,
    ) -> None:
        """Test start_compose_stack returns r."""
        result = docker_manager.start_compose_stack("docker-compose.yml")
        tm.that(isinstance(result, r), eq=True)

    def test_cleanup_dirty_containers_empty(
        self,
        docker_manager: tk,
    ) -> None:
        """Test cleanup with no dirty containers."""
        docker_manager._dirty_containers.clear()
        result = docker_manager.cleanup_dirty_containers()
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == [], eq=True)


class TestFlextTestsDockerWorkerId:
    """Test worker_id functionality."""

    def test_default_worker_id(self) -> None:
        """Test default worker_id is 'master'."""
        manager = tk()
        manager._dirty_containers.clear()
        tm.that(manager.worker_id == "master", eq=True)

    def test_custom_worker_id(self) -> None:
        """Test custom worker_id."""
        manager = tk(worker_id="worker_1")
        manager._dirty_containers.clear()
        tm.that(manager.worker_id == "worker_1", eq=True)

    def test_state_file_includes_worker_id(self) -> None:
        """Test state file path includes worker_id."""
        manager = tk(worker_id="test_worker")
        manager._dirty_containers.clear()
        tm.that("test_worker" in str(manager._state_file), eq=True)


class TestFlextTestsDockerWorkspaceRoot:
    """Test workspace_root functionality."""

    def test_default_workspace_root(self) -> None:
        """Test default workspace_root is cwd."""
        manager = tk()
        manager._dirty_containers.clear()
        tm.that(manager.workspace_root == Path.cwd(), eq=True)

    def test_custom_workspace_root(self, tmp_path: Path) -> None:
        """Test custom workspace_root."""
        manager = tk(workspace_root=tmp_path)
        manager._dirty_containers.clear()
        tm.that(manager.workspace_root == tmp_path, eq=True)
