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

from flext_cli import u as cli_u

from flext_tests._models.spec import FlextTestsSpecModelsMixin
from flext_tests.docker import FlextTestsDocker

USAGE = "usage: flext-tests docker {ensure|verify|down} --spec <yaml> [--target <name>]"

ContainerSpec = FlextTestsSpecModelsMixin.ContainerSpec


def load_spec(path: Path) -> ContainerSpec:
    """Parse one YAML spec document into the typed model (exits on failure)."""
    read = cli_u.Cli.files_read_text(path)
    if read.failure:
        raise SystemExit(1)
    parsed = cli_u.Cli.yaml_parse(read.value)
    if parsed.failure:
        raise SystemExit(1)
    try:
        return ContainerSpec.model_validate(parsed.value)
    except Exception as exc:
        raise SystemExit(1) from exc


def resolve_targets(spec: ContainerSpec, target: str | None) -> list[str]:
    """Resolve the requested target names (all when omitted)."""
    if target is None:
        return list(spec.containers)
    if target not in spec.containers:
        raise SystemExit(1)
    return [target]


def run_ensure(path: Path, target: str | None) -> int:
    """Ensure every requested container is up, healthy, and sealed."""
    spec = load_spec(path)
    exit_code = 0
    for name in resolve_targets(spec, target):
        config = spec.containers[name].model_copy(update={"container_name": name})
        manager = FlextTestsDocker(target_config=config, repository_root=Path.cwd())
        ensured = manager.execute()
        if ensured.failure:
            exit_code = 1
            continue
    return exit_code


def run_verify(path: Path, target: str | None) -> int:
    """Read-only verification: up, healthy, sealed against the fingerprint."""
    spec = load_spec(path)
    exit_code = 0
    for name in resolve_targets(spec, target):
        config = spec.containers[name].model_copy(update={"container_name": name})
        manager = FlextTestsDocker(target_config=config, repository_root=Path.cwd())
        verified = manager.verify()
        if verified.failure:
            exit_code = 1
            continue
    return exit_code


def run_down(path: Path, target: str | None) -> int:
    """Stop the compose projects of the requested targets."""
    spec = load_spec(path)
    exit_code = 0
    for name in resolve_targets(spec, target):
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
    """Entry point: flext-tests docker <verb> --spec <yaml> [--target <name>]."""
    args = list(sys.argv[1:] if argv is None else argv)
    verbs = {"ensure": run_ensure, "verify": run_verify, "down": run_down}
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
