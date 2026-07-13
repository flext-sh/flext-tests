"""Private docker builder test mixins."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

import pytest

from flext_tests import FlextTestsDocker, c as flext_tests_c, m, tk, tm
from tests import c


class DockerBuildersMixin:
    """Docker builder tests."""

    def test_shared_containers_attribute(self) -> None:
        """Test canonical shared containers constant."""
        tm.that(c.Tests.SHARED_CONTAINERS, none=False)
        tm.that(c.Tests.SHARED_CONTAINERS, is_=dict)

    def test_shared_builder_resolves_target_config(self, tmp_path: Path) -> None:
        """Test shared() builds a resolved container target from constants."""
        manager = tk.shared("flext-oracle-db-test", workspace_root=tmp_path)
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq="flext-oracle-db-test")
        tm.that(
            target.compose_file, eq=tmp_path / "docker" / "docker-compose.oracle-db.yml"
        )

    def test_shared_builder_resolves_openldap_target(self, tmp_path: Path) -> None:
        """Test shared() resolves the centralized OpenLDAP container target."""
        manager = tk.shared("flext-openldap-test", workspace_root=tmp_path)
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq="flext-openldap-test")
        tm.that(
            target.compose_file, eq=tmp_path / "docker" / "docker-compose.openldap.yml"
        )
        tm.that(target.service, eq="openldap")
        tm.that(target.port, eq=3390)

    def test_compose_builder_resolves_target_config(self, tmp_path: Path) -> None:
        """Test compose() builds a resolved explicit container target."""
        manager = tk.compose(
            "docker-compose.yml",
            target=m.Tests.ContainerConfig(
                container_name="service-test", service="service-test", port=5432
            ),
            workspace_root=tmp_path,
        )
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq="service-test")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.yml")
        tm.that(target.port, eq=5432)

    def test_stack_builder_resolves_target_config(self, tmp_path: Path) -> None:
        """Test stack() builds a resolved explicit compose-stack target."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(
                container_name="stack-main", service="stack-main", port=3389
            ),
            workspace_root=tmp_path,
        )
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq="stack-main")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.stack.yml")
        tm.that(target.service, eq="stack-main")
        tm.that(target.port, eq=3389)

    def test_stack_builder_allows_stack_only_target(self, tmp_path: Path) -> None:
        """Test stack() supports lifecycle-only stacks without inspection target."""
        manager = tk.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(host=c.LOOPBACK_IP, port=25432),
            workspace_root=tmp_path,
        )
        tm.that(manager.target_config, none=False)
        target = manager.target_config
        tm.that(target, none=False)
        tm.that(target.container_name, eq=None)
        tm.that(target.port, eq=25432)

    def test_resolve_shared_target_raises_on_missing_compose_file(self) -> None:
        broken = {
            name: {**config} for name, config in c.Tests.SHARED_CONTAINERS.items()
        }
        del broken["flext-oracle-db-test"]["compose_file"]

        with patch.object(flext_tests_c.Tests, "SHARED_CONTAINERS", broken):
            with pytest.raises(ValueError, match="missing compose_file"):
                FlextTestsDocker._resolve_shared_target_config(
                    "flext-oracle-db-test", Path("/tmp")
                )
