# AUTO-GENERATED FILE — Regenerate with: make gen
"""Fixtures package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests._fixtures._enforcement_parts.build import (
        build_items as build_items,
    )
    from flext_tests._fixtures._enforcement_parts.config import (
        SessionConfig as SessionConfig,
        resolve_config as resolve_config,
    )
    from flext_tests._fixtures._enforcement_parts.discovery import (
        collected_project_names as collected_project_names,
        collected_validator_targets as collected_validator_targets,
        load_infra_report as load_infra_report,
    )
    from flext_tests._fixtures._enforcement_parts.validators import (
        build_tests_validator_items as build_tests_validator_items,
        dispatch_infra_detector as dispatch_infra_detector,
    )
    from flext_tests._fixtures.enforcement import (
        EnforcementBuildContext as EnforcementBuildContext,
        EnforcementCollector as EnforcementCollector,
        EnforcementContribution as EnforcementContribution,
        EnforcementItem as EnforcementItem,
        EnforcementViolationError as EnforcementViolationError,
        active_rules as active_rules,
        builder_for as builder_for,
        builders as builders,
        clear as clear,
        discover_workspace_root as discover_workspace_root,
        get as get,
        register as register,
        split_csv as split_csv,
        warning_categories as warning_categories,
    )
    from flext_tests._fixtures.markdown_validation import (
        MarkdownCodeBlockCollector as MarkdownCodeBlockCollector,
        MarkdownCodeBlockItem as MarkdownCodeBlockItem,
        MarkdownValidationError as MarkdownValidationError,
    )
    from flext_tests._fixtures.project_metadata import (
        project_metadata as project_metadata,
        project_tool_flext as project_tool_flext,
    )
    from flext_tests._fixtures.settings import (
        clean_container as clean_container,
        reset_settings as reset_settings,
        sample_data as sample_data,
        settings as settings,
        settings_factory as settings_factory,
        temp_dir as temp_dir,
        temp_file as temp_file,
        test_context as test_context,
        test_runtime as test_runtime,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("._enforcement_parts",),
    build_lazy_import_map(
        {
            "._enforcement_parts": ("_enforcement_parts",),
            "._enforcement_parts.build": ("build_items",),
            "._enforcement_parts.config": (
                "SessionConfig",
                "resolve_config",
            ),
            "._enforcement_parts.discovery": (
                "collected_project_names",
                "collected_validator_targets",
                "load_infra_report",
            ),
            "._enforcement_parts.validators": (
                "build_tests_validator_items",
                "dispatch_infra_detector",
            ),
            ".enforcement": (
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
            ),
            ".markdown_validation": (
                "MarkdownCodeBlockCollector",
                "MarkdownCodeBlockItem",
                "MarkdownValidationError",
            ),
            ".project_metadata": (
                "project_metadata",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
