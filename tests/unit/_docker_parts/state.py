"""Private docker host-scoped container-state test mixins."""

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from flext_tests import FlextTestsDocker, m, tm
from tests import u


def _unique_container() -> str:
    """One collision-free container name per test invocation."""
    return f"state-{uuid4().hex[:12]}"


class TestsFlextTestsDockerStateMixin:
    """Host-scoped container-state behaviour through the public facade."""

    def test_client_cached(self) -> None:
        """The Docker client is resolved once and reused."""
        manager = FlextTestsDocker()
        client1 = manager.client
        client2 = manager.client
        tm.that(client1 is client2, eq=True)

    def test_state_persists_between_instances_host_scoped(self, tmp_path: Path) -> None:
        """Dirty markers survive across instances: state is host-scoped."""
        container = _unique_container()
        manager = FlextTestsDocker(state_root=tmp_path / "docker-state")
        mark_result = manager.mark_container_dirty(container)
        _ = u.Tests.assert_success(mark_result)
        reloaded_manager = FlextTestsDocker(state_root=tmp_path / "docker-state")
        tm.that(reloaded_manager.container_dirty(container), eq=True)
        _ = reloaded_manager.mark_container_clean(container)

    def test_state_file_round_trips_the_typed_model(self, tmp_path: Path) -> None:
        """The per-container JSON file carries the full typed state."""
        container = _unique_container()
        manager = FlextTestsDocker(state_root=tmp_path / "docker-state")
        sealed = m.Tests.ContainerState(
            container_name=container,
            container_id="abc123",
            fingerprint="fp-1",
            sealed=True,
            dirty=False,
        )
        write_result = manager.seal_container_state(sealed)
        _ = u.Tests.assert_success(write_result)
        raw = manager.state_file_path_for(container).read_text(encoding="utf-8")
        restored = m.Tests.ContainerState.model_validate_json(raw)
        tm.that(restored.container_id, eq="abc123")
        tm.that(restored.fingerprint, eq="fp-1")
        tm.that(restored.sealed, eq=True)
        _ = manager.mark_container_clean(container)

    def test_corrupted_state_file_fails_loud(self, tmp_path: Path) -> None:
        """A corrupt state file raises instead of silently starting fresh."""
        container = _unique_container()
        manager = FlextTestsDocker(state_root=tmp_path / "docker-state")
        state_file = manager.state_file_path_for(container)
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text("{not-json", encoding="utf-8")
        try:
            import pytest

            with pytest.raises(ValueError, match="state"):
                _ = manager.container_dirty(container)
        finally:
            state_file.unlink(missing_ok=True)

    def test_absent_state_reads_as_clean(self) -> None:
        """A container with no state file is clean and unsealed."""
        container = _unique_container()
        manager = FlextTestsDocker()
        tm.that(manager.container_dirty(container), eq=False)

    def test_mark_container_dirty(self, docker_manager: FlextTestsDocker) -> None:
        """Test marking container as dirty."""
        container = _unique_container()
        result = docker_manager.mark_container_dirty(container)
        _ = u.Tests.assert_success(result)
        tm.that(docker_manager.container_dirty(container), eq=True)

    def test_mark_container_clean(self, docker_manager: FlextTestsDocker) -> None:
        """Test marking container as clean."""
        container = _unique_container()
        _ = docker_manager.mark_container_dirty(container)
        result = docker_manager.mark_container_clean(container)
        _ = u.Tests.assert_success(result)
        tm.that(docker_manager.container_dirty(container), eq=False)

    def test_container_dirty(self, docker_manager: FlextTestsDocker) -> None:
        """Test checking if container is dirty."""
        dirty_container = _unique_container()
        clean_container = _unique_container()
        _ = docker_manager.mark_container_dirty(dirty_container)
        tm.that(docker_manager.container_dirty(dirty_container), eq=True)
        tm.that(docker_manager.container_dirty(clean_container), eq=False)

    def test_dirty_containers(self, docker_manager: FlextTestsDocker) -> None:
        """Test getting list of dirty containers."""
        container_a = _unique_container()
        container_b = _unique_container()
        _ = docker_manager.mark_container_dirty(container_a)
        _ = docker_manager.mark_container_dirty(container_b)
        dirty = docker_manager.dirty_containers
        tm.that(dirty, len=2, has=[container_a, container_b])
