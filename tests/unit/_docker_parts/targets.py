"""Private docker target failure test mixins."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests import m, tk, tm
from tests import c, u

if TYPE_CHECKING:
    from pathlib import Path


class DockerTargetsMixin:
    """Docker target failure tests."""

    def test_execute_requires_target_config(self, docker_manager: tk) -> None:
        """Test execute fails fast when no DSL target has been configured."""
        result = docker_manager.execute()
        _ = u.Tests.assert_failure(result)
        tm.that(result.error, has="Docker target not configured")

    def test_execute_rejects_stack_only_target(self, tmp_path: Path) -> None:
        """Test execute rejects stack targets without inspection container."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(host=c.LOOPBACK_IP, port=25432),
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
            target=m.Tests.ContainerConfig(
                container_name="stack-main", service="stack-main", port=59999
            ),
            workspace_root=tmp_path,
        )
        result = manager.ready(max_wait=1)
        _ = u.Tests.assert_success(result)
        tm.that(result.value is False, eq=True)
