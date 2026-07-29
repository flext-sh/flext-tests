"""FlextTestsConfig — frozen config singleton for flext-tests (ADR-005 §7).

Business rules live in ``config/*.yaml`` under the ``Tests:`` key. Validated
branches are typed explicitly while unrelated domains remain open through the
``config.Tests`` namespace. Access is ``config.Tests.<domain>.<key>``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict

from flext_cli import FlextCliConfig
from flext_tests._constants.validator import FlextTestsConstantsValidator


class _PytestTimeoutPolicy(BaseModel):
    """Typed pytest timeout decisions owned by production configuration."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    required_configured_cap_count: Literal[1]
    allow_timeout_func_only: bool
    timeout_owned_ini_keys: frozenset[FlextTestsConstantsValidator.PytestTimeoutIniKey]


class _EnforcementConfig(BaseModel):
    """Typed enforcement configuration."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    pytest_timeout: _PytestTimeoutPolicy


class _TestsNamespace(BaseModel):
    """Open, frozen namespace with typed branches for governed domains."""

    model_config = ConfigDict(extra="allow", frozen=True)

    enforcement: _EnforcementConfig


class FlextTestsConfig(FlextCliConfig):
    """Tests config auto-loaded from ``config/*.yaml``."""

    Tests: _TestsNamespace


config: FlextTestsConfig = FlextTestsConfig.fetch_global()
"""Pre-instantiated frozen config singleton — ``from flext_tests import config``."""

__all__: list[str] = ["FlextTestsConfig", "config"]
