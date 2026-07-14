"""Behavioral tests for the FlextTestsDocker public DSL contract.

Two layers are covered:

* Pure DSL-contract behavior that needs no Docker daemon (configuration
  resolution and unconfigured-target error paths) — always executed.
* Real shared-container behavior that requires a live Docker daemon — skipped
  when the daemon is unavailable.

Every assertion targets observable public behavior: the ``r[T]`` outcome of
fallible operations, the public model state of the configured target, the
public fields of the returned container info, and the exceptions the public
factory promises. No private attribute, collaborator spying, or internal
patching is used.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import m, tk
from flext_tests import m, tk, tm
from tests import c


class TestsFlextTestsDockerIntegration:
    """Public DSL contract of ``FlextTestsDocker`` (``tk``)."""

    @staticmethod
    def _workspace_root() -> Path:
        return Path(__file__).resolve().parents[3]

    # ------------------------------------------------------------------
    # Pure DSL-contract behavior (no Docker daemon required)
    # ------------------------------------------------------------------

    @pytest.mark.parametrize("container_name", sorted(c.Tests.SHARED_CONTAINERS))
    def test_shared_resolves_target_config_from_shared_catalog(
        self, container_name: str
    ) -> None:
        """``tk.shared`` maps a catalog entry onto the public target config."""
        settings = c.Tests.SHARED_CONTAINERS[container_name]
        root = Path("/tmp/flext-docker-contract")

        docker = tk.shared(container_name, workspace_root=root)

        target = docker.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq=container_name)
        tm.that(target.service, eq=settings["service"])
        tm.that(target.port, eq=settings["port"])
        tm.that(target.host, eq=settings["host"])

    @pytest.mark.parametrize("container_name", sorted(c.Tests.SHARED_CONTAINERS))
    def test_shared_resolves_compose_file_against_workspace_root(
        self, container_name: str
    ) -> None:
        """Relative catalog compose files resolve to an absolute workspace path."""
        settings = c.Tests.SHARED_CONTAINERS[container_name]
        root = Path("/tmp/flext-docker-contract")

        target = tk.shared(container_name, workspace_root=root).target_config

        tm.that(target, none=False)
        tm.that(target.compose_file, none=False)
        assert target.compose_file.is_absolute()
        tm.that(target.compose_file, eq=root / str(settings["compose_file"]))

    def test_shared_rejects_unknown_container_with_value_error(self) -> None:
        """An unknown shared name is a caller contract error, not a silent value."""
        with pytest.raises(ValueError, match="Unknown shared container: not-a-name"):
            tk.shared("not-a-name", workspace_root=Path("/tmp/flext-docker-contract"))

    def test_compose_resolves_relative_file_against_workspace_root(self) -> None:
        """``tk.compose`` anchors a relative compose file to the workspace root."""
        root = Path("/tmp/flext-docker-contract")

        target = tk.compose("docker/custom.yml", workspace_root=root).target_config

        tm.that(target, none=False)
        tm.that(target.compose_file, eq=root / "docker" / "custom.yml")

    def test_compose_preserves_absolute_file_unchanged(self) -> None:
        """An absolute compose file is used verbatim by ``tk.compose``."""
        absolute = Path("/opt/stacks/custom.yml")

        target = tk.compose(
            absolute, workspace_root=Path("/tmp/flext-docker-contract")
        ).target_config

        tm.that(target, none=False)
        tm.that(target.compose_file, eq=absolute)

    @pytest.mark.parametrize(
        "operation",
        ["execute", "up", "down", "ready"],
        ids=["execute", "up", "down", "ready"],
    )
    def test_unconfigured_target_fails_with_guidance(self, operation: str) -> None:
        """Every DSL verb reports a failure result when no target is configured."""
        docker = tk(workspace_root=Path("/tmp/flext-docker-contract"))

        result = getattr(docker, operation)()

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="not configured")

    def test_execute_reports_failure_for_stack_without_inspection_container(
        self,
    ) -> None:
        """A compose-only target (no container name) cannot be inspected by execute."""
        config = m.Tests.ContainerConfig(compose_file=Path("/tmp/stack.yml"))
        docker = tk(
            workspace_root=Path("/tmp/flext-docker-contract"), target_config=config
        )

        result = docker.execute()

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="no inspection container")

    # ------------------------------------------------------------------
    # Real shared-container behavior (requires a live Docker daemon)
    # ------------------------------------------------------------------

    @pytest.mark.integration
    @pytest.mark.docker
    def test_execute_shared_oracle_container_returns_running_info(self) -> None:
        """The DSL starts the shared Oracle container and reports it running."""
        docker = tk.shared(
            "flext-oracle-db-test", workspace_root=self._workspace_root()
        )
        tm.that(docker.client, none=False)

        result = docker.execute()

        tm.ok(result)
        container = result.unwrap()
        tm.that(container.name, eq="flext-oracle-db-test")
        tm.that(container.status, eq=c.Tests.ContainerStatus.RUNNING)
        assert container.container_id
        assert container.image

    @pytest.mark.integration
    @pytest.mark.docker
    def test_execute_shared_oracle_container_is_idempotent(self) -> None:
        """Repeated DSL execution keeps the shared Oracle container running."""
        docker = tk.shared(
            "flext-oracle-db-test", workspace_root=self._workspace_root()
        )
        tm.that(docker.client, none=False)

        first = docker.execute()
        second = docker.execute()

        tm.ok(first)
        tm.ok(second)
        first_info = first.unwrap()
        second_info = second.unwrap()
        tm.that(first_info.name, eq=second_info.name)
        tm.that(second_info.status, eq=c.Tests.ContainerStatus.RUNNING)
