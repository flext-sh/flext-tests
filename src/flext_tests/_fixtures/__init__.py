# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Fixtures package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

# mro-i6nq.10: The package consumes its manifest's public-export contract.
from flext_tests._fixtures.__unit__ import (
    CHILD_MODULE_PATHS as _CHILD_MODULE_PATHS,
    EXCLUDED_LAZY_NAMES as _EXCLUDED_LAZY_NAMES,
    LAZY_ALIAS_GROUPS as _LAZY_ALIAS_GROUPS,
    LAZY_MODULES as _LAZY_MODULES,
    PUBLIC_EXPORTS as _PUBLIC_EXPORTS,
)

if TYPE_CHECKING:
    from flext_tests._fixtures import _enforcement_parts as _enforcement_parts
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

    # mro-i6nq.10: Static declaration mirrors the installer-owned runtime binding.
    __all__: tuple[str, ...]


_LAZY_IMPORTS = merge_lazy_imports(
    _CHILD_MODULE_PATHS,
    build_lazy_import_map(
        _LAZY_MODULES,
        alias_groups=_LAZY_ALIAS_GROUPS,
        sort_keys=False,
    ),
    exclude_names=_EXCLUDED_LAZY_NAMES,
    module_name=__name__,
)


# mro-i6nq.10: The installer publishes __all__ from the manifest's literal ABI.
install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=_PUBLIC_EXPORTS,
)
