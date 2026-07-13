# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Validator package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

# mro-i6nq.10: The package consumes its manifest's public-export contract.
from flext_tests._validator.__unit__ import (
    CHILD_MODULE_PATHS as _CHILD_MODULE_PATHS,
    EXCLUDED_LAZY_NAMES as _EXCLUDED_LAZY_NAMES,
    LAZY_ALIAS_GROUPS as _LAZY_ALIAS_GROUPS,
    LAZY_MODULES as _LAZY_MODULES,
    PUBLIC_EXPORTS as _PUBLIC_EXPORTS,
)

if TYPE_CHECKING:
    from flext_tests._validator import _orchestration_parts as _orchestration_parts
    from flext_tests._validator._orchestration_parts.validator_part_02 import (
        FlextTestsValidator as FlextTestsValidator,
    )
    from flext_tests._validator.bypass import (
        FlextValidatorBypass as FlextValidatorBypass,
    )
    from flext_tests._validator.imports import (
        FlextValidatorImports as FlextValidatorImports,
    )
    from flext_tests._validator.layer import FlextValidatorLayer as FlextValidatorLayer
    from flext_tests._validator.markdown import (
        FlextValidatorMarkdown as FlextValidatorMarkdown,
    )
    from flext_tests._validator.models import (
        FlextTestsValidatorModels as FlextTestsValidatorModels,
    )
    from flext_tests._validator.settings import (
        FlextValidatorSettings as FlextValidatorSettings,
    )
    from flext_tests._validator.tests import FlextValidatorTests as FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes as FlextValidatorTypes

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
