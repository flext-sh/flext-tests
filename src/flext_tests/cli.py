"""CLI facade for flext-tests — thin transport adapter.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli.services.cli import FlextCliCli


class FlextTestsCli(FlextCliCli):
    """Flext-tests CLI facade — extends flext-cli CLI."""


def main() -> None:
    """Entry point."""


__all__: tuple[str, ...] = ("FlextTestsCli",)
