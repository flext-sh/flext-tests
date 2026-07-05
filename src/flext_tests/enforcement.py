"""Public enforcement fixture facade for FLEXT packages."""

from __future__ import annotations

from flext_tests._fixtures.enforcement import (
    EnforcementBuildContext,
    EnforcementCollector,
    EnforcementContribution,
    EnforcementItem,
    EnforcementViolationError,
    active_rules,
    builder_for,
    builders,
    clear,
    discover_workspace_root,
    get,
    register,
    split_csv,
    warning_categories,
)

__all__: list[str] = [
    "EnforcementBuildContext",
    "EnforcementCollector",
    "EnforcementContribution",
    "EnforcementItem",
    "EnforcementViolationError",
    "active_rules",
    "builder_for",
    "builders",
    "clear",
    "discover_workspace_root",
    "get",
    "register",
    "split_csv",
    "warning_categories",
]
