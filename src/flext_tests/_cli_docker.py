"""Spec-driven docker provisioning CLI for flext-tests.

`flext-tests docker ensure|verify|down --spec <yaml> --target <name>`:
provisioning runs OUTSIDE the pytest deadline (custom.mk pre-test hooks),
so container startup never consumes the timed test budget. The same YAML
spec feeds the in-session plugin — one SSOT.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import sys
from pathlib import Path

from flext_cli import u

from flext_tests import FlextTestsDocker, m


class FlextTestsCliDocker:
    """Spec-driven docker provisioning CLI surface."""

    USAGE = (
        "usage: flext-tests docker {ensure|verify|down} --spec <yaml> [--target <name>]"
    )

    @staticmethod
    def load_spec(path: Path) -> m.Tests.ContainerSpec:
        """Parse one YAML spec document into the typed model (exits on failure).

        Returns:
            The resulting ``ContainerSpec``.

        Raises:
            SystemExit: If ``read.failure``; or if ``parsed.failure``; or if a
                ``Exception`` is caught.

        """
        read = u.Cli.files_read_text(path)
        if read.failure:
            raise SystemExit(1)
        parsed = u.Cli.yaml_parse(read.value)
        if parsed.failure:
            raise SystemExit(1)
        try:
            return m.Tests.ContainerSpec.model_validate(parsed.value)
        except Exception as exc:
            raise SystemExit(1) from exc

    @staticmethod
    def resolve_targets(
        spec: m.Tests.ContainerSpec,
        target: str | None,
    ) -> list[str]:
        """Resolve the requested target names (all when omitted).

        Returns:
            The resulting ``list[str]``.

        Raises:
            SystemExit: If ``target not in spec.containers``.

        """
        if target is None:
            return list(spec.containers)
        if target not in spec.containers:
            raise SystemExit(1)
        return [target]

    @staticmethod
    def run_ensure(path: Path, target: str | None) -> int:
        """Ensure every requested container is up, healthy, and sealed.

        Returns:
            The resulting ``int``.

        """
        spec = FlextTestsCliDocker.load_spec(path)
        exit_code = 0
        for name in FlextTestsCliDocker.resolve_targets(spec, target):
            config = spec.containers[name].model_copy(update={"container_name": name})
            manager = FlextTestsDocker(target_config=config, repository_root=Path.cwd())
            ensured = manager.execute()
            if ensured.failure:
                exit_code = 1
                continue
        return exit_code

    @staticmethod
    def run_verify(path: Path, target: str | None) -> int:
        """Read-only verification: up, healthy, sealed against the fingerprint.

        Returns:
            The resulting ``int``.

        """
        spec = FlextTestsCliDocker.load_spec(path)
        exit_code = 0
        for name in FlextTestsCliDocker.resolve_targets(spec, target):
            config = spec.containers[name].model_copy(update={"container_name": name})
            manager = FlextTestsDocker(target_config=config, repository_root=Path.cwd())
            verified = manager.verify()
            if verified.failure:
                exit_code = 1
                continue
        return exit_code

    @staticmethod
    def run_down(path: Path, target: str | None) -> int:
        """Stop the compose projects of the requested targets.

        Returns:
            The resulting ``int``.

        """
        spec = FlextTestsCliDocker.load_spec(path)
        exit_code = 0
        for name in FlextTestsCliDocker.resolve_targets(spec, target):
            config = spec.containers[name]
            if config.compose_file is None:
                exit_code = 1
                continue
            manager = FlextTestsDocker(target_config=config, repository_root=Path.cwd())
            stopped = manager.compose_down(str(config.compose_file))
            if stopped.failure:
                exit_code = 1
                continue
        return exit_code


def main(argv: list[str] | None = None) -> int:
    """Entry point: flext-tests docker <verb> --spec <yaml> [--target <name>].

    Returns:
        The resulting ``int``.

    """
    args = list(sys.argv[1:] if argv is None else argv)
    verbs = {
        "ensure": FlextTestsCliDocker.run_ensure,
        "verify": FlextTestsCliDocker.run_verify,
        "down": FlextTestsCliDocker.run_down,
    }
    minimum_args = 3  # docker <verb> --spec <path>
    if len(args) < minimum_args or args[0] != "docker" or args[1] not in verbs:
        return 2
    spec_path: Path | None = None
    target: str | None = None
    rest = args[2:]
    index = 0
    while index < len(rest):
        if rest[index] == "--spec" and index + 1 < len(rest):
            spec_path = Path(rest[index + 1])
            index += 2
        elif rest[index] == "--target" and index + 1 < len(rest):
            target = rest[index + 1]
            index += 2
        else:
            return 2
    if spec_path is None:
        return 2
    return verbs[args[1]](spec_path, target)
