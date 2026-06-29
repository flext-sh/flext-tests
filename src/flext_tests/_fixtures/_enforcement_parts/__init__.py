# AUTO-GENERATED FILE — Regenerate with: make gen
"""Enforcement Parts package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
