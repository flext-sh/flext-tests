"""Private docker operation test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_infra import config as infra_config

from flext_tests import FlextTestsDocker, tm
from tests import c, u


class TestsFlextTestsDockerOperationsMixin:
    """Docker operation tests."""

    @staticmethod
    def test_compose_down_returns_flext_result(
        docker_manager: FlextTestsDocker,
    ) -> None:
        """Test compose_down failure behavior for missing compose file."""
        result = docker_manager.compose_down("missing-compose.yml")
        _ = u.Tests.assert_failure(result)

    @staticmethod
    def test_start_existing_container_not_found(
        docker_manager: FlextTestsDocker,
    ) -> None:
        """Test starting a container returns a failure result when unavailable."""
        result = docker_manager.start_existing_container("nonexistent_container")
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, is_=str)

    @staticmethod
    def test_fetch_container_info_not_found(
        docker_manager: FlextTestsDocker,
    ) -> None:
        """Test fetching container info returns a failure result when unavailable."""
        result = docker_manager.fetch_container_info("nonexistent_container")
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, is_=str)

    @staticmethod
    def test_fetch_container_status(docker_manager: FlextTestsDocker) -> None:
        """Test fetch_container_status delegates to container lookup."""
        result = docker_manager.fetch_container_status("nonexistent")
        _ = u.Tests.assert_failure(result)

    @staticmethod
    def test_wait_for_port_ready_immediate(
        docker_manager: FlextTestsDocker,
    ) -> None:
        """Test wait_for_port_ready fails closed quickly for unavailable port."""
        result = docker_manager.wait_for_port_ready(c.LOOPBACK_IP, 59999, max_wait=1)
        _ = u.Tests.assert_failure(result)
        tm.that(result.error or "", has="not ready")

    @staticmethod
    def test_cleanup_dirty_containers_empty(
        docker_manager: FlextTestsDocker,
    ) -> None:
        """A host without dirty records recreates nothing."""
        ci_variable = infra_config.Infra.codegen.make.ci.variable
        with u.Tests.env_vars_context(vars_to_clear=(ci_variable,)):
            result = docker_manager.cleanup_dirty_containers()
        _ = u.Tests.assert_success(result)
        tm.that(result.value, empty=True)

    @staticmethod
    def test_cleanup_dirty_containers_keeps_foreign_records(
        docker_manager: FlextTestsDocker,
    ) -> None:
        """A dirty record of an undeclared container is left to its own owner."""
        foreign = "foreign-owner-test"
        _ = u.Tests.assert_success(docker_manager.mark_container_dirty(foreign))
        ci_variable = infra_config.Infra.codegen.make.ci.variable
        with u.Tests.env_vars_context(vars_to_clear=(ci_variable,)):
            result = docker_manager.cleanup_dirty_containers()
        _ = u.Tests.assert_success(result)
        tm.that(result.value, empty=True)
        tm.that(docker_manager.container_dirty(foreign), eq=True)

    @staticmethod
    def test_default_state_dir_is_host_scoped() -> None:
        """Without an explicit directory the records live in the host directory."""
        host_dir = Path.home().joinpath(*c.Tests.DOCKER_STATE_DIR_PARTS)
        tm.that(u.Tests.docker_state_dir(), eq=host_dir)
        tm.that(FlextTestsDocker().state_dir, eq=host_dir)

    @staticmethod
    def test_builders_bind_the_given_state_dir(tmp_path: Path) -> None:
        """Every builder carries an explicit state directory to the facade."""
        state_dir = tmp_path / "state"
        shared = FlextTestsDocker.shared(
            "flext-openldap-test",
            repository_root=tmp_path,
            state_dir=state_dir,
        )
        composed = FlextTestsDocker.compose(
            "docker-compose.yml",
            repository_root=tmp_path,
            state_dir=state_dir,
        )
        tm.that(shared.state_dir, eq=state_dir)
        tm.that(composed.state_dir, eq=state_dir)

    @staticmethod
    def test_default_repository_root() -> None:
        """Test default repository_root is cwd."""
        manager = FlextTestsDocker()
        tm.that(manager.repository_root, eq=Path.cwd())

    @staticmethod
    def test_custom_repository_root(tmp_path: Path) -> None:
        """Test custom repository_root."""
        manager = FlextTestsDocker(repository_root=tmp_path)
        tm.that(manager.repository_root, eq=tmp_path)
