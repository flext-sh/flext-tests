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

from flext_tests import m, tk, tm
from tests import c, u


class TestsFlextTestsDocker:
    """Test suite for c.Tests.ContainerStatus enum."""

    def test_container_status_values(self) -> None:
        """Test c.Tests.ContainerStatus enum values."""
        tm.that(c.Tests.ContainerStatus.RUNNING.value, eq="running")
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

    @pytest.fixture
    def docker_manager(self, tmp_path: Path) -> tk:
        """Create a tk instance for testing."""
        fixtures_dir = Path(__file__).parent.parent.parent / "fixtures"
        manager = tk(workspace_root=fixtures_dir, worker_id=f"test-{tmp_path.name}")
        _ = manager.mark_container_clean("container1")
        _ = manager.mark_container_clean("container2")
        _ = manager.mark_container_clean("test_container")
        _ = manager.mark_container_clean("dirty_container")
        return manager

    def test_init(self, docker_manager: tk) -> None:
        """Test tk initialization."""
        assert isinstance(docker_manager, tk)
        tm.that(docker_manager.workspace_root, none=False)
        tm.that(docker_manager.dirty_containers, is_=list)

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
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
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

    def test_shared_containers_attribute(self) -> None:
        """Test canonical shared containers constant."""
        tm.that(c.Tests.SHARED_CONTAINERS, none=False)
        tm.that(c.Tests.SHARED_CONTAINERS, is_=dict)

    def test_shared_builder_resolves_target_config(self, tmp_path: Path) -> None:
        """Test shared() builds a resolved container target from constants."""
        manager = tk.shared("flext-oracle-db-test", workspace_root=tmp_path)
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        assert target is not None
        tm.that(target.container_name, eq="flext-oracle-db-test")
        tm.that(
            target.compose_file,
            eq=tmp_path / "docker" / "docker-compose.oracle-db.yml",
        )

    def test_shared_builder_resolves_openldap_target(self, tmp_path: Path) -> None:
        """Test shared() resolves the centralized OpenLDAP container target."""
        manager = tk.shared("flext-openldap-test", workspace_root=tmp_path)
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        assert target is not None
        tm.that(target.container_name, eq="flext-openldap-test")
        tm.that(
            target.compose_file,
            eq=tmp_path / "docker" / "docker-compose.openldap.yml",
        )
        tm.that(target.service, eq="openldap")
        tm.that(target.port, eq=3390)

    def test_compose_builder_resolves_target_config(self, tmp_path: Path) -> None:
        """Test compose() builds a resolved explicit container target."""
        manager = tk.compose(
            "docker-compose.yml",
            container_name="service-test",
            service="service-test",
            port=5432,
            workspace_root=tmp_path,
        )
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        assert target is not None
        tm.that(target.container_name, eq="service-test")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.yml")
        tm.that(target.port, eq=5432)

    def test_stack_builder_resolves_target_config(self, tmp_path: Path) -> None:
        """Test stack() builds a resolved explicit compose-stack target."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            container_name="stack-main",
            service="stack-main",
            port=3389,
            workspace_root=tmp_path,
        )
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        assert target is not None
        tm.that(target.container_name, eq="stack-main")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.stack.yml")
        tm.that(target.service, eq="stack-main")
        tm.that(target.port, eq=3389)

    def test_stack_builder_allows_stack_only_target(self, tmp_path: Path) -> None:
        """Test stack() supports lifecycle-only stacks without inspection target."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            host=c.LOOPBACK_IP,
            port=25432,
            workspace_root=tmp_path,
        )
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        assert target is not None
        tm.that(target.container_name, eq=None)
        tm.that(target.port, eq=25432)

    def test_execute_requires_target_config(self, docker_manager: tk) -> None:
        """Test execute fails fast when no DSL target has been configured."""
        result = docker_manager.execute()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_execute_rejects_stack_only_target(self, tmp_path: Path) -> None:
        """Test execute rejects stack targets without inspection container."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            host=c.LOOPBACK_IP,
            port=25432,
            workspace_root=tmp_path,
        )
        result = manager.execute()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="no inspection container")

    def test_up_requires_target_config(self, docker_manager: tk) -> None:
        """Test up fails fast when no DSL target has been configured."""
        result = docker_manager.up()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_down_requires_target_config(self, docker_manager: tk) -> None:
        """Test down fails fast when no DSL target has been configured."""
        result = docker_manager.down()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_ready_requires_target_config(self, docker_manager: tk) -> None:
        """Test ready fails fast when no DSL target has been configured."""
        result = docker_manager.ready()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_ready_uses_target_config_port(self, tmp_path: Path) -> None:
        """Test ready uses the configured target host and port."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            container_name="stack-main",
            service="stack-main",
            port=59999,
            workspace_root=tmp_path,
        )
        result = manager.ready(max_wait=1)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)

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
