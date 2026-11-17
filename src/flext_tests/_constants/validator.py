"""Enforcement dispatch constants for flext-tests (data-only facade).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar


class FlextTestsConstantsValidator:
    """Workspace discovery and engine-finding keys of the enforcement dispatch."""

    ENFORCEMENT_WORKSPACE_MARKERS: ClassVar[Sequence[str]] = (
        "AGENTS.md",
        "flext-core",
        "flext-tests",
    )
    ENFORCEMENT_PROJECT_PREFIX: ClassVar[str] = "flext-"
    ENFORCEMENT_PROJECT_MANIFEST: ClassVar[str] = "pyproject.toml"
    """Manifest that declares a standalone internal project."""
    ENFORCEMENT_PROJECT_DEPENDENCY: ClassVar[str] = "flext-core"
    """Distribution whose declared dependency marks an internal project."""
    ENFORCEMENT_PROJECT_KIND: ClassVar[str] = "internal_flext"
    """Explicit project kind accepted in ``tool.flext.kind``."""
    ENFORCEMENT_MANIFEST_ENCODING: ClassVar[str] = "utf-8"
    """Manifest encoding (stdlib TOML requires text)."""
    ENFORCEMENT_FINDING_SEVERITY_KEY: ClassVar[str] = "severity"
    """ast-grep JSON finding key carrying the rule severity."""
    ENFORCEMENT_FINDING_MESSAGE_KEY: ClassVar[str] = "message"
    """ast-grep JSON finding key carrying the rule message."""
    ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION: ClassVar[str] = "flext_slow_timeout_seconds"
    """Ini option carrying the config-owned timeout for slow pytest items."""
    ENFORCEMENT_SLOW_REPORT_TITLE: ClassVar[str] = "flext slow tests"
    """Title of the end-of-session section criticizing slow pytest items."""
    ENFORCEMENT_SLOW_NEAR_LIMIT_RATIO: ClassVar[float] = 0.8
    """Share of the slow budget from which a slow item is reported as near it."""
    ENFORCEMENT_SLOW_MARKER: ClassVar[str] = "slow"
    """Marker name declaring one pytest item explicitly slow."""
    ENFORCEMENT_HEAVY_TIER_MARKERS: ClassVar[Sequence[str]] = (
        "integration",
        "e2e",
        "performance",
        "docker",
        "oracle",
        "ldap",
    )
    """Declared heavy tiers and capability markers that run on the slow budget.

    Capability-heavy items provision shared services during setup, so the unit
    budget would expire before the service is usable; they share the
    config-owned slow budget instead of carrying a per-file marker.
    """
    ENFORCEMENT_TIMEOUT_OPTION: ClassVar[str] = "timeout"
    """pytest-timeout option carrying the ordinary per-item limit in seconds."""
    ENFORCEMENT_CALL_PHASE: ClassVar[str] = "call"
    """Report phase whose native duration the slow report measures."""
    ENFORCEMENT_DISPATCHER_MODULE: ClassVar[str] = (
        "flext_tests._fixtures._enforcement.dispatcher"
    )
    """Module the ``pytest11`` enforcement adapter resolves inside its hooks."""
    FIXTURE_PLUGIN_MODULES: ClassVar[Sequence[str]] = (
        "flext_tests._fixtures.settings",
        "flext_tests._fixtures.namespace",
        "flext_tests._fixtures.scratch_storage",
        "flext_tests._fixtures.fixture_trees",
    )
    """Fixture modules the ``pytest11`` fixture adapter registers at configure."""
    CAPABILITY_PLUGIN_MODULE: ClassVar[str] = "flext_tests._fixtures.connectivity"
    """Module owning the capability-gating plugin and its registration name."""


__all__: list[str] = ["FlextTestsConstantsValidator"]
