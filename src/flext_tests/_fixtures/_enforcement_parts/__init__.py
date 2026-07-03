# AUTO-GENERATED FILE — Regenerate with: make gen
"""Enforcement Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._fixtures._enforcement_parts.config import (
        active_rules as active_rules,
        discover_workspace_root as discover_workspace_root,
        split_csv as split_csv,
    )
    from flext_tests._fixtures._enforcement_parts.items import (
        EnforcementCollector as EnforcementCollector,
        EnforcementItem as EnforcementItem,
        EnforcementViolationError as EnforcementViolationError,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".build": ("build",),
        ".config": (
            "active_rules",
            "discover_workspace_root",
            "split_csv",
        ),
        ".discovery": ("discovery",),
        ".hooks": ("hooks",),
        ".items": (
            "EnforcementCollector",
            "EnforcementItem",
            "EnforcementViolationError",
        ),
        ".validators": ("validators",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
