# AUTO-GENERATED FILE — Regenerate with: make gen
"""Matchers Parts package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".data_driven": ("data_driven",),
        ".fail_constraints": ("fail_constraints",),
        ".ok_constraints": ("ok_constraints",),
        ".predicates": ("predicates",),
        ".results": ("results",),
        ".scope_errors": ("scope_errors",),
        ".that_attrs": ("that_attrs",),
        ".that_collections": ("that_collections",),
        ".validation": ("validation",),
        "flext_tests": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "td",
            "tf",
            "tk",
            "tm",
            "tv",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
