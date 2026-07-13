# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Fixtures. Enforcement Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

# mro-i6nq.10: The package consumes its manifest's public-export contract.
from flext_tests._fixtures._enforcement_parts.__unit__ import (
    LAZY_ALIAS_GROUPS as _LAZY_ALIAS_GROUPS,
    LAZY_MODULES as _LAZY_MODULES,
    PUBLIC_EXPORTS as _PUBLIC_EXPORTS,
)

if TYPE_CHECKING:
    from flext_tests._fixtures._enforcement_parts import hooks as hooks
    from flext_tests._fixtures._enforcement_parts.build import (
        build_items as build_items,
    )
    from flext_tests._fixtures._enforcement_parts.config import (
        SessionConfig as SessionConfig,
        active_rules as active_rules,
        discover_workspace_root as discover_workspace_root,
        resolve_config as resolve_config,
        split_csv as split_csv,
    )
    from flext_tests._fixtures._enforcement_parts.discovery import (
        collected_project_names as collected_project_names,
        collected_validator_targets as collected_validator_targets,
        load_infra_report as load_infra_report,
    )
    from flext_tests._fixtures._enforcement_parts.items import (
        EnforcementCollector as EnforcementCollector,
        EnforcementItem as EnforcementItem,
        EnforcementViolationError as EnforcementViolationError,
    )
    from flext_tests._fixtures._enforcement_parts.registry import (
        EnforcementBuildContext as EnforcementBuildContext,
        EnforcementContribution as EnforcementContribution,
        builder_for as builder_for,
        builders as builders,
        clear as clear,
        get as get,
        register as register,
        warning_categories as warning_categories,
    )
    from flext_tests._fixtures._enforcement_parts.validators import (
        build_tests_validator_items as build_tests_validator_items,
        dispatch_infra_detector as dispatch_infra_detector,
    )

    # mro-i6nq.10: Static declaration mirrors the installer-owned runtime binding.
    __all__: tuple[str, ...]


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES,
    alias_groups=_LAZY_ALIAS_GROUPS,
    sort_keys=False,
)


# mro-i6nq.10: The installer publishes __all__ from the manifest's literal ABI.
install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=_PUBLIC_EXPORTS,
)
