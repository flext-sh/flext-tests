"""Private docker operation test mixins."""

from __future__ import annotations

from pathlib import Path

from flext_tests import FlextTestsDocker, tm
from tests import c, u


class TestsFlextTestsDockerOperationsMixin:
    """Docker operation tests."""

    def test_compose_down_returns_flext_result(
        self, docker_manager: FlextTestsDocker
    ) -> None:
        """Test compose_down failure behavior for missing compose file."""
        result = docker_manager.compose_down("missing-compose.yml")
        _ = u.Tests.assert_failure(result)

    def test_start_existing_container_not_found(
        self, docker_manager: FlextTestsDocker
    ) -> None:
        """Test starting a container returns a failure result when unavailable."""
        result = docker_manager.start_existing_container("nonexistent_container")
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, is_=str)

    def test_fetch_container_info_not_found(
        self, docker_manager: FlextTestsDocker
    ) -> None:
        """Test fetching container info returns a failure result when unavailable."""
        result = docker_manager.fetch_container_info("nonexistent_container")
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, is_=str)

    def test_fetch_container_status(self, docker_manager: FlextTestsDocker) -> None:
        """Test fetch_container_status delegates to container lookup."""
        result = docker_manager.fetch_container_status("nonexistent")
        _ = u.Tests.assert_failure(result)

    def test_wait_for_port_ready_immediate(
        self, docker_manager: FlextTestsDocker
    ) -> None:
        """Test wait_for_port_ready fails closed quickly for unavailable port."""
        result = docker_manager.wait_for_port_ready(c.LOOPBACK_IP, 59999, max_wait=1)
        _ = u.Tests.assert_failure(result)
        tm.that(result.error or "", has="not ready")

    def test_cleanup_dirty_containers_empty(self, tmp_path: Path) -> None:
        """Test cleanup with no dirty containers in a fresh state tree."""
        manager = FlextTestsDocker(state_root=tmp_path / "docker-state")
        result = manager.cleanup_dirty_containers()
        _ = u.Tests.assert_success(result)
        tm.that(result.value, empty=True)

    def test_cleanup_dirty_containers_removes_stale_shared_entry(
        self, tmp_path: Path
    ) -> None:
        """Test cleanup purges retired shared containers from persisted state."""
        manager = FlextTestsDocker(
            repository_root=tmp_path, state_root=tmp_path / "docker-state"
        )
        _ = manager.mark_container_dirty("retired-shared-entry")

        result = manager.cleanup_dirty_containers()

        _ = u.Tests.assert_success(result)
        tm.that(result.value, empty=True)
        tm.that(manager.container_dirty("retired-shared-entry"), eq=False)

    def test_state_is_shared_across_manager_instances(self, tmp_path: Path) -> None:
        """Host-scoped state: a second manager sees the first's markers."""
        state_root = tmp_path / "docker-state"
        manager_a = FlextTestsDocker(state_root=state_root)
        _ = manager_a.mark_container_dirty("shared-container")
        manager_b = FlextTestsDocker(state_root=state_root)
        tm.that(manager_b.container_dirty("shared-container"), eq=True)

    def test_default_repository_root(self) -> None:
        """Test default repository_root is cwd."""
        manager = FlextTestsDocker()
        tm.that(manager.repository_root, eq=Path.cwd())

    def test_custom_repository_root(self, tmp_path: Path) -> None:
        """Test custom repository_root."""
        manager = FlextTestsDocker(repository_root=tmp_path)
        tm.that(manager.repository_root, eq=tmp_path)
