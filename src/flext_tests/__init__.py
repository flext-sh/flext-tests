# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
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

if _t.TYPE_CHECKING:
    from flext_infra import d as d, e as e, h as h, r as r, x as x
    from flext_tests._fixtures.enforcement import (
        EnforcementCollector as EnforcementCollector,
        EnforcementItem as EnforcementItem,
        EnforcementViolationError as EnforcementViolationError,
        active_rules as active_rules,
        discover_workspace_root as discover_workspace_root,
        split_csv as split_csv,
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
    from flext_tests._utilities.matchers import tm as tm
    from flext_tests.base import (
        FlextService as FlextService,
        FlextTestsCase as FlextTestsCase,
        FlextTestsServiceBase as FlextTestsServiceBase,
        s as s,
    )
    from flext_tests.constants import FlextTestsConstants as FlextTestsConstants, c as c
    from flext_tests.docker import tk as tk
    from flext_tests.domains import td as td
    from flext_tests.files import FlextTestsFiles as FlextTestsFiles, tf as tf
    from flext_tests.models import FlextTestsModels as FlextTestsModels, m as m
    from flext_tests.protocols import FlextTestsProtocols as FlextTestsProtocols, p as p
    from flext_tests.settings import FlextTestsSettings as FlextTestsSettings
    from flext_tests.typings import FlextTestsTypes as FlextTestsTypes, t as t
    from flext_tests.utilities import FlextTestsUtilities as FlextTestsUtilities, u as u
    from flext_tests.validator import tv as tv
_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._docker_parts.docker_part_06": ("FlextTestsDocker",),
        "._domains_parts.domains_part_03": ("FlextTestsDomains",),
        "._fixtures.enforcement": (
            "EnforcementCollector",
            "EnforcementItem",
            "EnforcementViolationError",
            "active_rules",
            "discover_workspace_root",
            "split_csv",
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
        "._utilities.matchers": ("tm",),
        "._validator._orchestration_parts.validator_part_02": ("FlextTestsValidator",),
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
        ".docker": ("tk",),
        ".domains": ("td",),
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
        ".settings": ("FlextTestsSettings",),
        ".typings": (
            "FlextTestsTypes",
            "t",
        ),
        ".utilities": (
            "FlextTestsUtilities",
            "u",
        ),
        ".validator": ("tv",),
        "flext_infra": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)


__all__: tuple[str, ...] = (
    "EnforcementCollector",
    "EnforcementItem",
    "EnforcementViolationError",
    "FlextService",
    "FlextTestsCase",
    "FlextTestsConstants",
    "FlextTestsFiles",
    "FlextTestsModels",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsSettings",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "MarkdownCodeBlockCollector",
    "MarkdownCodeBlockItem",
    "MarkdownValidationError",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "active_rules",
    "c",
    "clean_container",
    "d",
    "discover_workspace_root",
    "e",
    "h",
    "m",
    "p",
    "project_metadata",
    "project_namespace_config",
    "project_tool_flext",
    "r",
    "reset_settings",
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
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
