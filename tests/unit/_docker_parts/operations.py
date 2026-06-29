"""Private docker operation test mixins."""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import tk, tm
from tests.constants import c
from tests.utilities import u


class DockerOperationsMixin:
    """Docker operation tests."""

    def test_compose_up_returns_flext_result(
        self,
        docker_manager: tk,
    ) -> None:
        """Test compose_up returns a valid public Result contract."""
        result = docker_manager.compose_up("missing-compose.yml")
        tm.that(result.success or result.failure, eq=True)
        if result.success:
            tm.that(result.value, is_=str)
        else:
            tm.that(result.error, is_=str)

    def test_compose_down_returns_flext_result(
        self,
        docker_manager: tk,
    ) -> None:
        """Test compose_down failure behavior for missing compose file."""
        result = docker_manager.compose_down("missing-compose.yml")
        _ = u.Tests.assert_failure(result)

    def test_start_existing_container_not_found(
        self,
        docker_manager: tk,
    ) -> None:
        """Test starting a container returns a failure result when unavailable."""
        result = docker_manager.start_existing_container("nonexistent_container")
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, is_=str)

    def test_fetch_container_info_not_found(
        self,
        docker_manager: tk,
    ) -> None:
        """Test fetching container info returns a failure result when unavailable."""
        result = docker_manager.fetch_container_info("nonexistent_container")
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, is_=str)

    def test_fetch_container_status(self, docker_manager: tk) -> None:
        """Test fetch_container_status delegates to container lookup."""
        result = docker_manager.fetch_container_status("nonexistent")
        _ = u.Tests.assert_failure(result)

    def test_wait_for_port_ready_immediate(
        self,
        docker_manager: tk,
    ) -> None:
        """Test wait_for_port_ready returns quickly for unavailable port."""
        result = docker_manager.wait_for_port_ready(
            c.LOOPBACK_IP,
            59999,
            max_wait=1,
        )
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)

    def test_start_compose_stack_returns_result(
        self,
        docker_manager: tk,
    ) -> None:
        """Test start_compose_stack returns a valid public Result contract."""
        result = docker_manager.start_compose_stack("missing-compose.yml")
        tm.that(result.success or result.failure, eq=True)
        if result.success:
            tm.that(result.value, is_=str)
        else:
            tm.that(result.error, is_=str)

    def test_cleanup_dirty_containers_empty(
        self,
        docker_manager: tk,
    ) -> None:
        """Test cleanup with no dirty containers."""
        _ = docker_manager.mark_container_clean("container1")
        _ = docker_manager.mark_container_clean("container2")
        result = docker_manager.cleanup_dirty_containers()
        _ = u.Tests.assert_success(result)
        tm.that(result.value, empty=True)

    def test_default_worker_id(self) -> None:
        """Test default worker_id is 'master'."""
        manager = tk()
        tm.that(manager.worker_id, eq="master")

    def test_custom_worker_id(self) -> None:
        """Test custom worker_id."""
        manager = tk(worker_id="worker_1")
        tm.that(manager.worker_id, eq="worker_1")

    def test_worker_id_isolates_persisted_dirty_state(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Test different worker_id values isolate persisted dirty state."""
        monkeypatch.setenv("HOME", str(tmp_path))
        manager_a = tk(worker_id="worker_a")
        _ = manager_a.mark_container_dirty("container-x")
        manager_b = tk(worker_id="worker_b")
        tm.that(manager_b.container_dirty("container-x"), eq=False)
        manager_a_reload = tk(worker_id="worker_a")
        tm.that(manager_a_reload.container_dirty("container-x"), eq=True)

    def test_default_workspace_root(self) -> None:
        """Test default workspace_root is cwd."""
        manager = tk()
        tm.that(manager.workspace_root, eq=Path.cwd())

    def test_custom_workspace_root(self, tmp_path: Path) -> None:
        """Test custom workspace_root."""
        manager = tk(workspace_root=tmp_path)
        tm.that(manager.workspace_root, eq=tmp_path)
