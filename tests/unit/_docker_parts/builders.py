"""Private docker builder test mixins."""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker, m, tm
from tests import c


class TestsFlextTestsDockerBuildersMixin:
    """Docker builder tests."""

    @pytest.mark.parametrize("container_name", sorted(c.Tests.SHARED_CONTAINERS))
    def test_shared_builder_resolves_every_declared_container(
        self, container_name: str, tmp_path: Path
    ) -> None:
        """shared() resolves each declared container from the constants SSOT."""
        declared = c.Tests.SHARED_CONTAINERS[container_name]
        manager = FlextTestsDocker.shared(container_name, repository_root=tmp_path)
        target = tm.not_none(manager.target_config)
        tm.that(target.container_name, eq=container_name)
        tm.that(target.compose_file, eq=tmp_path / str(declared["compose_file"]))
        tm.that(target.service, eq=declared["service"])
        tm.that(target.port, eq=declared["port"])

    def test_compose_builder_resolves_target_config(self, tmp_path: Path) -> None:
        """Test compose() builds a resolved explicit container target."""
        manager = FlextTestsDocker.compose(
            "docker-compose.yml",
            target=m.Tests.ContainerConfig(
                container_name="service-test", service="service-test", port=5432
            ),
            repository_root=tmp_path,
        )
        target = tm.not_none(manager.target_config)
        tm.that(target.container_name, eq="service-test")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.yml")
        tm.that(target.port, eq=5432)

    def test_stack_builder_resolves_target_config(self, tmp_path: Path) -> None:
        """Test stack() builds a resolved explicit compose-stack target."""
        manager = FlextTestsDocker.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(
                container_name="stack-main", service="stack-main", port=3389
            ),
            repository_root=tmp_path,
        )
        target = tm.not_none(manager.target_config)
        tm.that(target.container_name, eq="stack-main")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.stack.yml")
        tm.that(target.service, eq="stack-main")
        tm.that(target.port, eq=3389)

    def test_stack_builder_allows_stack_only_target(self, tmp_path: Path) -> None:
        """Test stack() supports lifecycle-only stacks without inspection target."""
        manager = FlextTestsDocker.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(host=c.LOOPBACK_IP, port=25432),
            repository_root=tmp_path,
        )
        target = tm.not_none(manager.target_config)
        tm.that(target.container_name, eq=None)
        tm.that(target.port, eq=25432)

    def test_resolve_shared_target_raises_on_unknown_container(
        self, tmp_path: Path
    ) -> None:
        """Unknown shared containers fail loud against the real constants SSOT."""
        with pytest.raises(ValueError, match="Unknown shared container"):
            FlextTestsDocker.shared(
                "no-such-shared-container", repository_root=tmp_path
            )
