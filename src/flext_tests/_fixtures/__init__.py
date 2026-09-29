# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Fixtures package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import _enforcement_parts
    from ._enforcement_parts.build import FlextTestsEnforcementBuilder
    from ._enforcement_parts.dispatcher import FlextTestsEnforcementDispatcher
    from ._enforcement_parts.items import FlextTestsEnforcementItem
    from ._enforcement_parts.namespace import NamespaceDetectorBuilder
    from ._enforcement_parts.validators import FlextTestsEnforcementValidators
    from ._markdown_collector import FlextTestsMarkdownCodeBlockCollector
    from ._markdown_error import FlextTestsMarkdownValidationError
    from .connectivity import FlextTestsConnectivityPlugin
    from .markdown_validation import FlextTestsMarkdownCodeBlockItem
    from .project_metadata import project_metadata, project_tool_flext
    from .settings import (
        clean_container,
        reset_settings,
        sample_data,
        settings,
        settings_factory,
        temp_dir,
        temp_file,
        test_context,
        test_runtime,
    )


__all__: tuple[str, ...] = (
    "FlextTestsConnectivityPlugin",
    "FlextTestsEnforcementBuilder",
    "FlextTestsEnforcementDispatcher",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementValidators",
    "FlextTestsMarkdownCodeBlockCollector",
    "FlextTestsMarkdownCodeBlockItem",
    "FlextTestsMarkdownValidationError",
    "NamespaceDetectorBuilder",
    "_enforcement_parts",
    "clean_container",
    "project_metadata",
    "project_tool_flext",
    "reset_settings",
    "sample_data",
    "settings",
    "settings_factory",
    "temp_dir",
    "temp_file",
    "test_context",
    "test_runtime",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._enforcement_parts": ("_enforcement_parts",),
            "._enforcement_parts.build": ("FlextTestsEnforcementBuilder",),
            "._enforcement_parts.dispatcher": ("FlextTestsEnforcementDispatcher",),
            "._enforcement_parts.items": ("FlextTestsEnforcementItem",),
            "._enforcement_parts.namespace": ("NamespaceDetectorBuilder",),
            "._enforcement_parts.validators": ("FlextTestsEnforcementValidators",),
            "._markdown_collector": ("FlextTestsMarkdownCodeBlockCollector",),
            "._markdown_error": ("FlextTestsMarkdownValidationError",),
            ".connectivity": ("FlextTestsConnectivityPlugin",),
            ".markdown_validation": ("FlextTestsMarkdownCodeBlockItem",),
            ".project_metadata": ("project_metadata", "project_tool_flext"),
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
