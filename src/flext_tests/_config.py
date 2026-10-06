"""FlextTestsConfig — frozen config singleton for flext-tests (ADR-005 §7).

Model-less: business rules live in ``config/*.yaml`` under the ``Tests:`` key and
are exposed through the open ``config.Tests`` namespace (``extra="allow"``), with
no per-domain model. Access is ``config.Tests.<domain>[<key>...]``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import FlextCliConfig

import flext_tests._models._tests_namespace
from flext_tests import m


class FlextTestsConfig(FlextCliConfig):
    """Tests config auto-loaded model-less from ``config/*.yaml``."""

    Tests: Annotated[
        flext_tests._models._tests_namespace._TestsNamespace,
        m.Field(
            description="Open namespace exposing ``config/*.yaml`` under ``Tests``.",
        ),
    ] = flext_tests._models._tests_namespace._TestsNamespace()


config: FlextTestsConfig = FlextTestsConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_tests import config``."""

__all__: list[str] = ["FlextTestsConfig", "config"]
