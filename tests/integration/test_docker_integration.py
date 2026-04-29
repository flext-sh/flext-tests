"""Integration tests for FlextTestsDocker using a real shared container."""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import tk
from tests import c


def _workspace_root() -> Path:
    return Path(__file__).resolve().parents[3]


@pytest.mark.integration
@pytest.mark.docker
def test_execute_shared_oracle_container_returns_running_info() -> None:
    """Ensure the Docker DSL starts the shared Oracle container and reports it running."""
    docker = tk.shared("flext-oracle-db-test", workspace_root=_workspace_root())
    if docker.client is None:
        pytest.skip(docker.client_error or "Docker client unavailable")

    result = docker.execute()

    assert result.success, result.error
    container = result.unwrap()
    assert container.name == "flext-oracle-db-test"
    assert container.status == c.Tests.ContainerStatus.RUNNING
    assert container.container_id
    assert container.image


@pytest.mark.integration
@pytest.mark.docker
def test_execute_shared_oracle_container_is_idempotent() -> None:
    """Ensure repeated DSL execution keeps the shared Oracle container usable."""
    docker = tk.shared("flext-oracle-db-test", workspace_root=_workspace_root())
    if docker.client is None:
        pytest.skip(docker.client_error or "Docker client unavailable")

    first = docker.execute()
    second = docker.execute()

    assert first.success, first.error
    assert second.success, second.error
    assert first.unwrap().name == second.unwrap().name
    assert second.unwrap().status == c.Tests.ContainerStatus.RUNNING
