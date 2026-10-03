"""Behavioral tests for the FlextTestsDocker public DSL contract.

The DSL contract needs no Docker daemon: configuration resolution and the
error paths of an unconfigured target. The lifecycle against a real daemon is
covered by ``test_docker_lifecycle.py``.

Every assertion targets observable public behavior: the ``r[T]`` outcome of
fallible operations, the public model state of the configured target, the
public fields of the returned container info, and the exceptions the public
factory promises. No private attribute, collaborator spying, or internal
patching is used.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker, m, tm
from tests import c, u


class TestsFlextTestsDockerIntegration:
    """Public DSL contract of ``FlextTestsDocker`` (``FlextTestsDocker``)."""

    @staticmethod
    def _repository_root() -> Path:
        return Path(__file__).resolve().parents[2]

    # ------------------------------------------------------------------
    # Pure DSL-contract behavior (no Docker daemon required)
    # ------------------------------------------------------------------

    @staticmethod
    @pytest.mark.parametrize("container_name", sorted(c.Tests.SHARED_CONTAINERS))
    def test_shared_resolves_target_config_from_shared_catalog(
        container_name: str,
        tmp_path: Path,
    ) -> None:
        """``FlextTestsDocker.shared`` maps a catalog entry onto the public target config."""
        settings = c.Tests.SHARED_CONTAINERS[container_name]
        root = tmp_path / "flext-docker-contract"

        docker = FlextTestsDocker.shared(container_name, repository_root=root)

        target = tm.not_none(docker.target_config)
        tm.that(target.container_name, eq=container_name)
        tm.that(target.service, eq=settings["service"])
        tm.that(target.port, eq=settings["port"])
        tm.that(target.host, eq=settings["host"])

    @staticmethod
    @pytest.mark.parametrize("container_name", sorted(c.Tests.SHARED_CONTAINERS))
    def test_shared_resolves_compose_file_against_repository_root(
        container_name: str,
        tmp_path: Path,
    ) -> None:
        """Relative catalog compose files resolve to an absolute workspace path."""
        settings = c.Tests.SHARED_CONTAINERS[container_name]
        root = tmp_path / "flext-docker-contract"

        target = tm.not_none(
            FlextTestsDocker.shared(container_name, repository_root=root).target_config,
        )
        compose_file = tm.not_none(target.compose_file)

        tm.that(compose_file.is_absolute(), eq=True)
        tm.that(compose_file, eq=root / str(settings["compose_file"]))

    @staticmethod
    def test_shared_rejects_unknown_container_with_value_error(
        tmp_path: Path,
    ) -> None:
        """An unknown shared name is a caller contract error, not a silent value."""
        with pytest.raises(ValueError, match="Unknown shared container: not-a-name"):
            FlextTestsDocker.shared(
                "not-a-name",
                repository_root=tmp_path / "flext-docker-contract",
            )

    @staticmethod
    def test_compose_resolves_relative_file_against_repository_root(
        tmp_path: Path,
    ) -> None:
        """``FlextTestsDocker.compose`` anchors a relative compose file to the workspace root."""
        root = tmp_path / "flext-docker-contract"

        target = tm.not_none(
            FlextTestsDocker.compose(
                "docker/custom.yml",
                repository_root=root,
            ).target_config,
        )
        tm.that(target.compose_file, eq=root / "docker" / "custom.yml")

    @staticmethod
    def test_sibling_compose_files_use_distinct_projects(tmp_path: Path) -> None:
        """Each compose file binds to its own project name.

        Compose derives the project from the parent directory when none is set,
        so sibling stacks in ``docker/`` would share one project and
        ``remove_orphans`` would delete another suite's container.
        """
        root = tmp_path / "flext-docker-contract" / "docker"
        oracle_file = tm.not_none(
            FlextTestsDocker.compose(
                root / "docker-compose.oracle-db.yml",
                repository_root=root,
            ).target_config,
        ).compose_file
        openldap_file = tm.not_none(
            FlextTestsDocker.compose(
                root / "docker-compose.openldap.yml",
                repository_root=root,
            ).target_config,
        ).compose_file

        tm.that(
            u.Tests.docker_compose_project(tm.not_none(oracle_file)),
            eq="docker-compose-oracle-db",
        )
        tm.that(
            u.Tests.docker_compose_project(tm.not_none(openldap_file)),
            eq="docker-compose-openldap",
        )

    @staticmethod
    def test_compose_preserves_absolute_file_unchanged(tmp_path: Path) -> None:
        """An absolute compose file is used verbatim by ``FlextTestsDocker.compose``."""
        absolute = Path("/opt/stacks/custom.yml")

        target = tm.not_none(
            FlextTestsDocker.compose(
                absolute,
                repository_root=tmp_path / "flext-docker-contract",
            ).target_config,
        )
        tm.that(target.compose_file, eq=absolute)

    @staticmethod
    @pytest.mark.parametrize(
        "operation",
        ["execute", "up", "down", "ready"],
        ids=["execute", "up", "down", "ready"],
    )
    def test_unconfigured_target_fails_with_guidance(
        operation: str,
        tmp_path: Path,
    ) -> None:
        """Every DSL verb reports a failure result when no target is configured."""
        docker = FlextTestsDocker(repository_root=tmp_path / "flext-docker-contract")

        result = getattr(docker, operation)()

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="not configured")

    @staticmethod
    def test_execute_reports_failure_for_stack_without_inspection_container(
        tmp_path: Path,
    ) -> None:
        """A compose-only target (no container name) cannot be inspected by execute."""
        config = m.Tests.ContainerConfig(compose_file=tmp_path / "stack.yml")
        docker = FlextTestsDocker(
            repository_root=tmp_path / "flext-docker-contract",
            target_config=config,
        )

        result = docker.execute()

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="no inspection container")
