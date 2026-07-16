"""Private docker state and model test mixins."""

from __future__ import annotations

from flext_tests import tk, tm
from tests import c, m, p, u
from pathlib import Path

import pytest


class DockerStateMixin:
    """Docker state and model tests."""

    def test_container_status_values(self) -> None:
        """Test c.Tests.ContainerStatus enum values."""
        tm.that(c.Tests.ContainerStatus.CREATED.value, eq="created")
        tm.that(c.Tests.ContainerStatus.RUNNING.value, eq="running")
        tm.that(c.Tests.ContainerStatus.EXITED.value, eq="exited")
        tm.that(c.Tests.ContainerStatus.PAUSED.value, eq="paused")
        tm.that(c.Tests.ContainerStatus.REMOVING.value, eq="removing")
        tm.that(c.Tests.ContainerStatus.DEAD.value, eq="dead")
        tm.that(c.Tests.ContainerStatus.STOPPED.value, eq="stopped")
        tm.that(c.Tests.ContainerStatus.NOT_FOUND.value, eq="not_found")
        tm.that(c.Tests.ContainerStatus.ERROR.value, eq="error")

    def test_container_info_creation(self) -> None:
        """Test container info model creation with required fields."""
        info = m.Tests.ContainerInfo(
            name="test_container",
            status=c.Tests.ContainerStatus.RUNNING,
            ports={"8080/tcp": "8080"},
            image="nginx:latest",
        )
        tm.that(info.name, eq="test_container")
        tm.that(info.status, eq=c.Tests.ContainerStatus.RUNNING.value)
        tm.that(info.ports, eq={"8080/tcp": "8080"})
        tm.that(info.image, eq="nginx:latest")
        tm.that(not info.container_id, eq=True)

    def test_container_info_with_container_id(self) -> None:
        """Test container info model with container_id."""
        info = m.Tests.ContainerInfo(
            name="test_container",
            status=c.Tests.ContainerStatus.RUNNING,
            ports={},
            image="nginx:latest",
            container_id="abc123",
        )
        tm.that(info.container_id, eq="abc123")

    def test_init(self, docker_manager: tk) -> None:
        """Test tk initialization."""
        tm.that(docker_manager, is_=tk)
        tm.that(docker_manager.workspace_root, none=False)
        tm.that(docker_manager.dirty_containers, is_=tuple)

    def test_client_initialization(self) -> None:
        """Test Docker client lazy initialization."""
        manager = tk()
        client = manager.client
        tm.that(client is None or hasattr(client, "containers"), eq=True)

    def test_client_cached(self) -> None:
        """Test Docker client caching."""
        manager = tk()
        client1 = manager.client
        client2 = manager.client
        tm.that(client1 is client2, eq=True)

    def test_dirty_state_persists_between_instances(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Test dirty-state persistence through public API across instances."""
        monkeypatch.setenv("HOME", str(tmp_path))
        worker_id = "persist-worker"
        manager = tk(worker_id=worker_id)
        mark_result = manager.mark_container_dirty("container1")
        _ = u.Tests.assert_success(mark_result)
        reloaded_manager = tk(worker_id=worker_id)
        tm.that(reloaded_manager.container_dirty("container1"), eq=True)

    def test_mark_container_dirty(self, docker_manager: tk) -> None:
        """Test marking container as dirty."""
        result = docker_manager.mark_container_dirty("test_container")
        _ = u.Tests.assert_success(result)
        tm.that(docker_manager.container_dirty("test_container"), eq=True)

    def test_mark_container_clean(self, docker_manager: tk) -> None:
        """Test marking container as clean."""
        _ = docker_manager.mark_container_dirty("test_container")
        result = docker_manager.mark_container_clean("test_container")
        _ = u.Tests.assert_success(result)
        tm.that(not docker_manager.container_dirty("test_container"), eq=True)

    def test_container_dirty(self, docker_manager: tk) -> None:
        """Test checking if container is dirty."""
        _ = docker_manager.mark_container_dirty("dirty_container")
        tm.that(docker_manager.container_dirty("dirty_container"), eq=True)
        tm.that(not docker_manager.container_dirty("clean_container"), eq=True)

    def test_dirty_containers(self, docker_manager: tk) -> None:
        """Test getting list of dirty containers."""
        _ = docker_manager.mark_container_dirty("container1")
        _ = docker_manager.mark_container_dirty("container2")
        dirty = docker_manager.dirty_containers
        tm.that(len(dirty), eq=2)
        tm.that(dirty, has="container1")
        tm.that(dirty, has="container2")
