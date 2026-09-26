"""Private docker dirty-state test mixins."""

from __future__ import annotations

from flext_tests import FlextTestsDocker, tm
from tests import u


class TestsFlextTestsDockerStateMixin:
    """Docker dirty-state behaviour through the public facade."""

    def test_client_cached(self) -> None:
        """The Docker client is resolved once and reused."""
        manager = FlextTestsDocker()
        client1 = manager.client
        client2 = manager.client
        tm.that(client1 is client2, eq=True)

    def test_dirty_state_persists_between_instances(self) -> None:
        """Test dirty-state persistence through public API across instances."""
        worker_id = "persist-worker"
        manager = FlextTestsDocker(worker_id=worker_id)
        mark_result = manager.mark_container_dirty("container1")
        _ = u.Tests.assert_success(mark_result)
        reloaded_manager = FlextTestsDocker(worker_id=worker_id)
        tm.that(reloaded_manager.container_dirty("container1"), eq=True)

    def test_mark_container_dirty(self, docker_manager: FlextTestsDocker) -> None:
        """Test marking container as dirty."""
        result = docker_manager.mark_container_dirty("test_container")
        _ = u.Tests.assert_success(result)
        tm.that(docker_manager.container_dirty("test_container"), eq=True)

    def test_mark_container_clean(self, docker_manager: FlextTestsDocker) -> None:
        """Test marking container as clean."""
        _ = docker_manager.mark_container_dirty("test_container")
        result = docker_manager.mark_container_clean("test_container")
        _ = u.Tests.assert_success(result)
        tm.that(docker_manager.container_dirty("test_container"), eq=False)

    def test_container_dirty(self, docker_manager: FlextTestsDocker) -> None:
        """Test checking if container is dirty."""
        _ = docker_manager.mark_container_dirty("dirty_container")
        tm.that(docker_manager.container_dirty("dirty_container"), eq=True)
        tm.that(docker_manager.container_dirty("clean_container"), eq=False)

    def test_dirty_containers(self, docker_manager: FlextTestsDocker) -> None:
        """Test getting list of dirty containers."""
        _ = docker_manager.mark_container_dirty("container1")
        _ = docker_manager.mark_container_dirty("container2")
        dirty = docker_manager.dirty_containers
        tm.that(dirty, len=2, has=["container1", "container2"])
