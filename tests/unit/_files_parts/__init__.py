# AUTO-GENERATED FILE — Regenerate with: make gen
"""Files Parts package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".assert_exists": ("assert_exists",),
        ".batch_create_in": ("batch_create_in",),
        ".compare": ("compare",),
        ".content_meta": ("content_meta",),
        ".contexts": ("contexts",),
        ".creation": ("creation",),
        ".formats": ("formats",),
        ".info_cleanup": ("info_cleanup",),
        ".info_metadata": ("info_metadata",),
        ".read": ("read",),
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
