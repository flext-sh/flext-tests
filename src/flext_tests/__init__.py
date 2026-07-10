# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_tests.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_infra import d as d, e as e, h as h, r as r, x as x
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
        project_namespace_config as project_namespace_config,
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
    from flext_tests.base import (
        FlextService as FlextService,
        FlextTestsCase as FlextTestsCase,
        FlextTestsServiceBase as FlextTestsServiceBase,
        s as s,
    )
    from flext_tests.constants import FlextTestsConstants as FlextTestsConstants, c as c
    from flext_tests.docker import FlextTestsDocker as FlextTestsDocker, tk as tk
    from flext_tests.domains import FlextTestsDomains as FlextTestsDomains, td as td
    from flext_tests.files import FlextTestsFiles as FlextTestsFiles, tf as tf
    from flext_tests.models import FlextTestsModels as FlextTestsModels, m as m
    from flext_tests.protocols import FlextTestsProtocols as FlextTestsProtocols, p as p
    from flext_tests.tmatchers import (
        FlextTestsMatchersUtilities as FlextTestsMatchersUtilities,
        tm as tm,
    )
    from flext_tests.typings import FlextTestsTypes as FlextTestsTypes, t as t
    from flext_tests.utilities import FlextTestsUtilities as FlextTestsUtilities, u as u
    from flext_tests.validator import (
        FlextTestsValidator as FlextTestsValidator,
        tv as tv,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._docker_parts",
        "._domains_parts",
        "._validator",
    ),
    build_lazy_import_map(
        {
            "._settings": ("FlextTestsSettings", "settings"),
            "._fixtures._enforcement_parts.build": ("build_items",),
            "._fixtures._enforcement_parts.config": (
                "SessionConfig",
                "resolve_config",
            ),
            "._fixtures._enforcement_parts.discovery": (
                "collected_project_names",
                "collected_validator_targets",
                "load_infra_report",
            ),
            "._fixtures._enforcement_parts.validators": (
                "build_tests_validator_items",
                "dispatch_infra_detector",
            ),
            "._fixtures.enforcement": (
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
            "._fixtures.markdown_validation": (
                "MarkdownCodeBlockCollector",
                "MarkdownCodeBlockItem",
                "MarkdownValidationError",
            ),
            "._fixtures.project_metadata": (
                "project_metadata",
                "project_namespace_config",
                "project_tool_flext",
            ),
            "._fixtures.settings": (
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
            "._validator._markdown_parts.markdown_part_02": ("FlextValidatorMarkdown",),
            "._validator._types_parts.types_part_02": ("FlextValidatorTypes",),
            "._validator.bypass": ("FlextValidatorBypass",),
            "._validator.imports": ("FlextValidatorImports",),
            "._validator.layer": ("FlextValidatorLayer",),
            "._validator.models": ("FlextTestsValidatorModels",),
            "._validator.settings": ("FlextValidatorSettings",),
            "._validator.tests": ("FlextValidatorTests",),
            ".base": (
                "FlextService",
                "FlextTestsCase",
                "FlextTestsServiceBase",
                "s",
            ),
            ".constants": (
                "FlextTestsConstants",
                "c",
            ),
            ".docker": (
                "FlextTestsDocker",
                "tk",
            ),
            ".domains": (
                "FlextTestsDomains",
                "td",
            ),
            ".files": (
                "FlextTestsFiles",
                "tf",
            ),
            ".models": (
                "FlextTestsModels",
                "m",
            ),
            ".protocols": (
                "FlextTestsProtocols",
                "p",
            ),
            ".tmatchers": (
                "FlextTestsMatchersUtilities",
                "tm",
            ),
            ".typings": (
                "FlextTestsTypes",
                "t",
            ),
            ".utilities": (
                "FlextTestsUtilities",
                "u",
            ),
            ".validator": (
                "FlextTestsValidator",
                "tv",
            ),
            "flext_infra": (
                "d",
                "e",
                "h",
                "r",
                "x",
            ),
        },
    ),
    exclude_names=(
        "_markdown_parts",
        "_orchestration_parts",
        "_settings_parts",
        "_types_parts",
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


__all__: tuple[str, ...] = (
    "FlextTestsSettings",
    "settings",
    "EnforcementBuildContext",
    "EnforcementCollector",
    "EnforcementContribution",
    "EnforcementItem",
    "EnforcementViolationError",
    "FlextService",
    "FlextTestsCase",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsFiles",
    "FlextTestsMatchersUtilities",
    "FlextTestsModels",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidator",
    "MarkdownCodeBlockCollector",
    "MarkdownCodeBlockItem",
    "MarkdownValidationError",
    "SessionConfig",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "active_rules",
    "build_items",
    "build_tests_validator_items",
    "builder_for",
    "builders",
    "c",
    "clean_container",
    "clear",
    "collected_project_names",
    "collected_validator_targets",
    "d",
    "discover_workspace_root",
    "dispatch_infra_detector",
    "e",
    "get",
    "h",
    "load_infra_report",
    "m",
    "p",
    "project_metadata",
    "project_namespace_config",
    "project_tool_flext",
    "r",
    "register",
    "reset_settings",
    "resolve_config",
    "s",
    "sample_data",
    "settings",
    "settings_factory",
    "split_csv",
    "t",
    "td",
    "temp_dir",
    "temp_file",
    "test_context",
    "test_runtime",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "warning_categories",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
