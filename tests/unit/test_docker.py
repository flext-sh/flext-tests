"""Behavioral unit tests for the flext_tests Docker control facade (tk).

Every test asserts observable public behavior of the ``tk`` / ``FlextTestsDocker``
DSL: return values, ``r[T]`` success/failure outcomes, public model state, and
raised errors. No private attributes, internal collaborators, or patched
internals are exercised.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import tk, tm
from tests import c, m, p, u


@pytest.fixture
def docker_manager(tmp_path: Path) -> tk:
    """Create a tk instance with a known-clean container baseline."""
    fixtures_dir = Path(__file__).parent.parent.parent / "fixtures"
    manager = tk(workspace_root=fixtures_dir, worker_id=f"test-{tmp_path.name}")
    _ = manager.mark_container_clean("container1")
    _ = manager.mark_container_clean("container2")
    _ = manager.mark_container_clean("test_container")
    _ = manager.mark_container_clean("dirty_container")
    return manager


class TestsFlextTestsDocker:
    """Behavioral contract of the Docker control facade (tk)."""

    # ------------------------------------------------------------------ #
    # ContainerStatus enum + ContainerInfo model public state            #
    # ------------------------------------------------------------------ #

    @pytest.mark.parametrize(
        ("member", "expected_value"),
        [
            (c.Tests.ContainerStatus.CREATED, "created"),
            (c.Tests.ContainerStatus.RUNNING, "running"),
            (c.Tests.ContainerStatus.EXITED, "exited"),
            (c.Tests.ContainerStatus.PAUSED, "paused"),
            (c.Tests.ContainerStatus.REMOVING, "removing"),
            (c.Tests.ContainerStatus.DEAD, "dead"),
            (c.Tests.ContainerStatus.STOPPED, "stopped"),
            (c.Tests.ContainerStatus.NOT_FOUND, "not_found"),
            (c.Tests.ContainerStatus.ERROR, "error"),
        ],
    )
    def test_container_status_exposes_stable_wire_value(
        self, member: c.Tests.ContainerStatus, expected_value: str
    ) -> None:
        """Each ContainerStatus member serializes to its documented string."""
        tm.that(member.value, eq=expected_value)

    def test_container_info_exposes_constructed_fields(self) -> None:
        """ContainerInfo publishes the fields it was built from."""
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

    def test_container_info_retains_container_id_when_provided(self) -> None:
        """An explicit container_id is preserved on the public model."""
        info = m.Tests.ContainerInfo(
            name="test_container",
            status=c.Tests.ContainerStatus.RUNNING,
            ports={},
            image="nginx:latest",
            container_id="abc123",
        )
        tm.that(info.container_id, eq="abc123")

    # ------------------------------------------------------------------ #
    # Construction defaults and public identity                          #
    # ------------------------------------------------------------------ #

    def test_new_manager_exposes_public_identity(self, docker_manager: tk) -> None:
        """A constructed manager reports its workspace and dirty tuple."""
        tm.that(docker_manager, is_=tk)
        tm.that(docker_manager.workspace_root, none=False)
        tm.that(docker_manager.dirty_containers, is_=tuple)

    def test_default_worker_id_is_master(self) -> None:
        """The default worker identity is 'master'."""
        tm.that(tk().worker_id, eq="master")

    def test_custom_worker_id_is_retained(self) -> None:
        """A supplied worker_id surfaces unchanged."""
        tm.that(tk(worker_id="worker_1").worker_id, eq="worker_1")

    def test_default_workspace_root_is_cwd(self) -> None:
        """Absent an override, workspace_root defaults to the cwd."""
        tm.that(tk().workspace_root, eq=Path.cwd())

    def test_custom_workspace_root_is_retained(self, tmp_path: Path) -> None:
        """A supplied workspace_root surfaces unchanged."""
        tm.that(tk(workspace_root=tmp_path).workspace_root, eq=tmp_path)

    def test_client_property_is_stable_across_reads(self) -> None:
        """The lazily-resolved client is the same object on repeated reads."""
        manager = tk()
        first = manager.client
        second = manager.client
        tm.that(first is second, eq=True)
        tm.that(first is None or hasattr(first, "containers"), eq=True)

    # ------------------------------------------------------------------ #
    # Dirty-state tracking behavior (public API round-trips)             #
    # ------------------------------------------------------------------ #

    def test_mark_dirty_makes_container_dirty(self, docker_manager: tk) -> None:
        """Marking a container dirty is observable via container_dirty."""
        result = docker_manager.mark_container_dirty("test_container")
        _ = u.Tests.assert_success(result)
        tm.that(docker_manager.container_dirty("test_container"), eq=True)

    def test_mark_clean_clears_dirty_flag(self, docker_manager: tk) -> None:
        """Marking a dirty container clean clears its dirty flag."""
        _ = docker_manager.mark_container_dirty("test_container")
        result = docker_manager.mark_container_clean("test_container")
        _ = u.Tests.assert_success(result)
        tm.that(not docker_manager.container_dirty("test_container"), eq=True)

    def test_unmarked_container_is_not_dirty(self, docker_manager: tk) -> None:
        """A container never marked dirty reports clean."""
        _ = docker_manager.mark_container_dirty("dirty_container")
        tm.that(docker_manager.container_dirty("dirty_container"), eq=True)
        tm.that(not docker_manager.container_dirty("clean_container"), eq=True)

    def test_dirty_containers_lists_all_marked(self, docker_manager: tk) -> None:
        """dirty_containers enumerates every currently-dirty container."""
        _ = docker_manager.mark_container_dirty("container1")
        _ = docker_manager.mark_container_dirty("container2")
        dirty = docker_manager.dirty_containers
        tm.that(len(dirty), eq=2)
        tm.that(dirty, has="container1")
        tm.that(dirty, has="container2")

    def test_dirty_state_persists_across_instances(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Dirty state survives a fresh manager for the same worker_id."""
        monkeypatch.setenv("HOME", str(tmp_path))
        worker_id = "persist-worker"
        manager = tk(worker_id=worker_id)
        _ = u.Tests.assert_success(manager.mark_container_dirty("container1"))
        reloaded = tk(worker_id=worker_id)
        tm.that(reloaded.container_dirty("container1"), eq=True)

    def test_worker_id_isolates_persisted_dirty_state(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Distinct worker_id values do not share persisted dirty state."""
        monkeypatch.setenv("HOME", str(tmp_path))
        worker_a = tk(worker_id="worker_a")
        _ = worker_a.mark_container_dirty("container-x")
        worker_b = tk(worker_id="worker_b")
        tm.that(worker_b.container_dirty("container-x"), eq=False)
        reloaded_a = tk(worker_id="worker_a")
        tm.that(reloaded_a.container_dirty("container-x"), eq=True)

    # ------------------------------------------------------------------ #
    # Fluent DSL builders resolve public target_config state             #
    # ------------------------------------------------------------------ #

    def test_shared_containers_constant_is_a_mapping(self) -> None:
        """The canonical shared-container catalog is a populated mapping."""
        tm.that(c.Tests.SHARED_CONTAINERS, none=False)
        tm.that(c.Tests.SHARED_CONTAINERS, is_=dict)

    def test_shared_resolves_oracle_target(self, tmp_path: Path) -> None:
        """shared() resolves the Oracle catalog entry into a target config."""
        manager = tk.shared("flext-oracle-db-test", workspace_root=tmp_path)
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq="flext-oracle-db-test")
        tm.that(
            target.compose_file, eq=tmp_path / "docker" / "docker-compose.oracle-db.yml"
        )

    def test_shared_resolves_openldap_target(self, tmp_path: Path) -> None:
        """shared() resolves the OpenLDAP catalog entry, incl. service/port."""
        manager = tk.shared("flext-openldap-test", workspace_root=tmp_path)
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq="flext-openldap-test")
        tm.that(
            target.compose_file, eq=tmp_path / "docker" / "docker-compose.openldap.yml"
        )
        tm.that(target.service, eq="openldap")
        tm.that(target.port, eq=3390)

    def test_shared_rejects_unknown_container(self) -> None:
        """shared() fails loudly for a container absent from the catalog."""
        with pytest.raises(ValueError, match="Unknown shared container"):
            _ = tk.shared("nonexistent-shared-container")

    def test_compose_resolves_explicit_target(self, tmp_path: Path) -> None:
        """compose() resolves an explicit target against the workspace root."""
        manager = tk.compose(
            "docker-compose.yml",
            target=m.Tests.ContainerConfig(
                container_name="service-test", service="service-test", port=5432
            ),
            workspace_root=tmp_path,
        )
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq="service-test")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.yml")
        tm.that(target.port, eq=5432)

    def test_stack_resolves_explicit_target(self, tmp_path: Path) -> None:
        """stack() resolves an explicit inspection target."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(
                container_name="stack-main", service="stack-main", port=3389
            ),
            workspace_root=tmp_path,
        )
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq="stack-main")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.stack.yml")
        tm.that(target.service, eq="stack-main")
        tm.that(target.port, eq=3389)

    def test_stack_allows_inspectionless_target(self, tmp_path: Path) -> None:
        """stack() supports lifecycle-only stacks with no inspection container."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(host=c.LOOPBACK_IP, port=25432),
            workspace_root=tmp_path,
        )
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq=None)
        tm.that(target.port, eq=25432)

    # ------------------------------------------------------------------ #
    # DSL lifecycle guards fail loudly without a configured target       #
    # ------------------------------------------------------------------ #

    def test_execute_without_target_fails(self, docker_manager: tk) -> None:
        """execute() fails when no DSL target has been configured."""
        result = docker_manager.execute()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_execute_on_inspectionless_stack_fails(self, tmp_path: Path) -> None:
        """execute() rejects a stack target with no inspection container."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(host=c.LOOPBACK_IP, port=25432),
            workspace_root=tmp_path,
        )
        result = manager.execute()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="no inspection container")

    def test_up_without_target_fails(self, docker_manager: tk) -> None:
        """up() fails when no DSL target has been configured."""
        result = docker_manager.up()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_down_without_target_fails(self, docker_manager: tk) -> None:
        """down() fails when no DSL target has been configured."""
        result = docker_manager.down()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_ready_without_target_fails(self, docker_manager: tk) -> None:
        """ready() fails when no DSL target has been configured."""
        result = docker_manager.ready()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_ready_uses_configured_target_port(self, tmp_path: Path) -> None:
        """ready() probes the configured target port and reports not-ready."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(
                container_name="stack-main", service="stack-main", port=59999
            ),
            workspace_root=tmp_path,
        )
        result = manager.ready(max_wait=1)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)

    # ------------------------------------------------------------------ #
    # Operations return honest r[T] outcomes (no hidden failures)        #
    # ------------------------------------------------------------------ #

    def test_compose_up_returns_result_contract(self, docker_manager: tk) -> None:
        """compose_up() returns a well-formed success-or-failure result."""
        result = docker_manager.compose_up("missing-compose.yml")
        tm.that(result.success or result.failure, eq=True)
        if result.success:
            tm.that(result.value, is_=str)
        else:
            tm.that(result.error, is_=str)

    def test_compose_down_missing_file_fails(self, docker_manager: tk) -> None:
        """compose_down() fails for a missing compose file."""
        result = docker_manager.compose_down("missing-compose.yml")
        _ = u.Tests.assert_failure(result)

    def test_start_missing_container_fails(self, docker_manager: tk) -> None:
        """start_existing_container() fails for an absent container."""
        result = docker_manager.start_existing_container("nonexistent_container")
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, is_=str)

    def test_fetch_missing_container_info_fails(self, docker_manager: tk) -> None:
        """fetch_container_info() fails for an absent container."""
        result = docker_manager.fetch_container_info("nonexistent_container")
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, is_=str)

    def test_fetch_missing_container_status_fails(self, docker_manager: tk) -> None:
        """fetch_container_status() fails for an absent container."""
        result = docker_manager.fetch_container_status("nonexistent")
        _ = u.Tests.assert_failure(result)

    def test_wait_for_closed_port_reports_not_ready(self, docker_manager: tk) -> None:
        """wait_for_port_ready() succeeds with False for a closed port."""
        result = docker_manager.wait_for_port_ready(c.LOOPBACK_IP, 59999, max_wait=1)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)

    def test_start_compose_stack_returns_result_contract(
        self, docker_manager: tk
    ) -> None:
        """start_compose_stack() returns a well-formed result."""
        result = docker_manager.start_compose_stack("missing-compose.yml")
        tm.that(result.success or result.failure, eq=True)
        if result.success:
            tm.that(result.value, is_=str)
        else:
            tm.that(result.error, is_=str)

    def test_cleanup_with_no_dirty_containers_is_empty(
        self, docker_manager: tk
    ) -> None:
        """cleanup_dirty_containers() returns an empty set when nothing is dirty."""
        _ = docker_manager.mark_container_clean("container1")
        _ = docker_manager.mark_container_clean("container2")
        result = docker_manager.cleanup_dirty_containers()
        _ = u.Tests.assert_success(result)
        tm.that(result.value, empty=True)

    def test_cleanup_purges_stale_shared_entry(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """Cleanup drops a dirty container absent from the shared catalog."""
        monkeypatch.setenv("HOME", str(tmp_path))
        manager = tk(workspace_root=tmp_path, worker_id="stale-container")
        _ = manager.mark_container_dirty("projeto_a-oud-test")
        result = manager.cleanup_dirty_containers()
        _ = u.Tests.assert_success(result)
        tm.that(result.value, empty=True)
        tm.that(manager.container_dirty("projeto_a-oud-test"), eq=False)
