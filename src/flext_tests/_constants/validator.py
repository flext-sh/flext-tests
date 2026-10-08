"""Enforcement dispatch constants for flext-tests (data-only facade).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from flext_cli import t


class FlextTestsConstantsValidator:
    """Workspace discovery and engine-finding keys of the enforcement dispatch."""

    ENFORCEMENT_WORKSPACE_MARKERS: ClassVar[t.StrSequence] = (
        "AGENTS.md",
        "flext-core",
        "flext-tests",
    )
    ENFORCEMENT_PROJECT_PREFIX: ClassVar[str] = "flext-"
    ENFORCEMENT_FINDING_SEVERITY_KEY: ClassVar[str] = "severity"
    """ast-grep JSON finding key carrying the rule severity."""
    ENFORCEMENT_FINDING_MESSAGE_KEY: ClassVar[str] = "message"
    """ast-grep JSON finding key carrying the rule message."""
    ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION: ClassVar[str] = "flext_slow_timeout_seconds"
    """Ini option carrying the config-owned timeout for slow pytest items."""
    ENFORCEMENT_DISPATCHER_MODULE: ClassVar[str] = (
        "flext_tests._fixtures._enforcement_parts.dispatcher"
    )
    """Module the ``pytest11`` enforcement adapter resolves inside its hooks."""
    FIXTURE_PLUGIN_MODULES: ClassVar[t.StrSequence] = (
        "flext_tests._fixtures.settings",
        "flext_tests._fixtures.namespace",
        "flext_tests._fixtures.scratch_storage",
    )
    """Fixture modules the ``pytest11`` fixture adapter registers at configure."""
    CAPABILITY_PLUGIN_MODULE: ClassVar[str] = "flext_tests._fixtures.connectivity"
    """Module owning the capability-gating plugin and its registration name."""


__all__: list[str] = ["FlextTestsConstantsValidator"]
