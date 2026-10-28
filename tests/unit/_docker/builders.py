"""Private docker builder test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_tests import FlextTestsDocker
from tests import c, m, tm, u


class TestsFlextTestsDockerBuildersMixin:
    """Docker builder tests."""

    @staticmethod
    def test_container_spec_roundtrip_retains_typed_targets() -> None:
        """The public spec owns the same target contract the Docker DSL consumes."""
        target_name = "spec-target"
        target = m.Tests.ContainerConfig(container_name=target_name)
        spec = m.Tests.ContainerSpec(containers={target_name: target})
        restored = m.Tests.ContainerSpec.model_validate_json(spec.model_dump_json())
        manager = FlextTestsDocker(target_config=restored.containers[target_name])
        resolved = tm.not_none(manager.target_config)
        tm.that(resolved.model_dump(), eq=target.model_dump())

    @staticmethod
    @pytest.mark.parametrize(
        ("verb", "document", "target", "succeeds"),
        [
            ("ensure", "containers: {}\n", None, True),
            ("verify", "containers: {}\n", None, True),
            ("down", "containers: {}\n", None, True),
            ("down", "containers: {}\n", "missing-target", False),
            ("down", "containers: []\n", None, False),
            ("down", "containers: {spec-target: {}}\n", "spec-target", False),
        ],
    )
    def test_spec_cli_validates_and_resolves_targets_without_docker(
        tmp_path: Path,
        verb: str,
        document: str,
        target: str | None,
        *,
        succeeds: bool,
    ) -> None:
        """The shipped CLI parses specs and rejects invalid targets before Docker."""
        spec_path = tmp_path / "containers.yaml"
        _ = tm.ok(u.Cli.files_write_text(spec_path, document))
        arguments = ["flext-tests", "docker", verb, "--spec", str(spec_path)]
        if target is not None:
            arguments.extend(("--target", target))
        output = tm.ok(u.Cli.run_raw(arguments, cwd=tmp_path))
        expected = c.Cli.EXIT_CODE_SUCCESS if succeeds else c.Cli.EXIT_CODE_FAILURE
        diagnostic = (
            f"{arguments!r}: outcome={output.outcome!r}; "
            f"stdout={output.stdout!r}; stderr={output.stderr!r}"
        )
        tm.that(output.outcome.timed_out, eq=False, msg=diagnostic)
        tm.that(output.outcome.forwarded_signal, eq=None, msg=diagnostic)
        tm.that(output.outcome.raw_return_code, eq=expected, msg=diagnostic)

    @staticmethod
    @pytest.mark.parametrize("container_name", sorted(c.Tests.SHARED_CONTAINERS))
    def test_shared_builder_resolves_every_declared_container(
        container_name: str,
        tmp_path: Path,
    ) -> None:
        """shared() resolves each declared container from the constants SSOT."""
        declared = c.Tests.SHARED_CONTAINERS[container_name]
        manager = FlextTestsDocker.shared(container_name, repository_root=tmp_path)
        target = tm.not_none(manager.target_config)
        tm.that(target.container_name, eq=container_name)
        tm.that(
            target.compose_file,
            eq=u.Tests.docker_shared_assets_dir() / str(declared["compose_file"]),
        )
        tm.that(target.service, eq=declared["service"])
        tm.that(target.port, eq=declared["port"])

    @staticmethod
    def test_compose_builder_resolves_target_config(tmp_path: Path) -> None:
        """Test compose() builds a resolved explicit container target."""
        manager = FlextTestsDocker.compose(
            "docker-compose.yml",
            target=m.Tests.ContainerConfig(
                container_name="service-test",
                service="service-test",
                port=5432,
            ),
            repository_root=tmp_path,
        )
        target = tm.not_none(manager.target_config)
        tm.that(target.container_name, eq="service-test")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.yml")
        tm.that(target.port, eq=5432)

    @staticmethod
    def test_stack_builder_resolves_target_config(tmp_path: Path) -> None:
        """Test stack() builds a resolved explicit compose-stack target."""
        manager = FlextTestsDocker.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(
                container_name="stack-main",
                service="stack-main",
                port=3389,
            ),
            repository_root=tmp_path,
        )
        target = tm.not_none(manager.target_config)
        tm.that(target.container_name, eq="stack-main")
        tm.that(target.compose_file, eq=tmp_path / "docker-compose.stack.yml")
        tm.that(target.service, eq="stack-main")
        tm.that(target.port, eq=3389)

    @staticmethod
    def test_stack_builder_allows_stack_only_target(tmp_path: Path) -> None:
        """Test stack() supports lifecycle-only stacks without inspection target."""
        manager = FlextTestsDocker.stack(
            "docker-compose.stack.yml",
            target=m.Tests.ContainerConfig(host=c.LOOPBACK_IP, port=25432),
            repository_root=tmp_path,
        )
        target = tm.not_none(manager.target_config)
        tm.that(target.container_name, eq=None)
        tm.that(target.port, eq=25432)

    @staticmethod
    def test_resolve_shared_target_raises_on_unknown_container(
        tmp_path: Path,
    ) -> None:
        """Unknown shared containers fail loud against the real constants SSOT."""
        with pytest.raises(ValueError, match="Unknown shared container"):
            FlextTestsDocker.shared(
                "no-such-shared-container",
                repository_root=tmp_path,
            )
