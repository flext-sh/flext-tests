"""CLI facade for flext-tests — thin transport adapter.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli.services.cli import FlextCliCli
from flext_tests._cli_docker import main as docker_main

from flext_tests._cli_docker import main as docker_main


class FlextTestsCli(FlextCliCli):
    """Flext-tests CLI facade — extends flext-cli CLI."""


def main() -> None:
    """Entry point: flext-tests docker <verb> --spec <yaml> [--target <name>].

    Raises:
        SystemExit: Always.
    """
    raise SystemExit(docker_main())


__all__: tuple[str, ...] = ("FlextTestsCli",)
