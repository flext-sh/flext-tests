# AUTO-GENERATED FILE — Regenerate with: make gen
"""Validator package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._markdown_parts",
        "._orchestration_parts",
        "._settings_parts",
        "._types_parts",
    ),
    build_lazy_import_map(
        {
            "._markdown_parts": ("_markdown_parts",),
            "._markdown_parts.markdown_part_02": ("FlextValidatorMarkdown",),
            "._orchestration_parts": ("_orchestration_parts",),
            "._orchestration_parts.validator_part_02": ("FlextTestsValidator",),
            "._settings_parts": ("_settings_parts",),
            "._types_parts": ("_types_parts",),
            "._types_parts.types_part_02": ("FlextValidatorTypes",),
            ".bypass": ("FlextValidatorBypass",),
            ".imports": ("FlextValidatorImports",),
            ".layer": ("FlextValidatorLayer",),
            ".models": ("FlextTestsValidatorModels",),
            ".settings": ("FlextValidatorSettings",),
            ".tests": ("FlextValidatorTests",),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
