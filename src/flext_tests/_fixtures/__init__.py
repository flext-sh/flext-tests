# AUTO-GENERATED FILE — Regenerate with: make gen
"""Fixtures package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".enforcement": (
            "EnforcementCollector",
            "EnforcementItem",
            "EnforcementViolationError",
        ),
        ".markdown_validation": (
            "MarkdownCodeBlockCollector",
            "MarkdownCodeBlockItem",
            "MarkdownValidationError",
        ),
        ".project_metadata": (
            "project_metadata",
            "project_namespace_config",
            "project_tool_flext",
        ),
        ".settings": (
            "clean_container",
            "reset_settings",
            "sample_data",
            "settings",
            "settings_factory",
            "temp_dir",
            "temp_file",
            "test_context",
            "test_runtime",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
