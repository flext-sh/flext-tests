# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Constants package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

# mro-i6nq.10: The package consumes its manifest's public-export contract.
from flext_tests._constants.__unit__ import (
    LAZY_ALIAS_GROUPS as _LAZY_ALIAS_GROUPS,
    LAZY_MODULES as _LAZY_MODULES,
    PUBLIC_EXPORTS as _PUBLIC_EXPORTS,
)

if TYPE_CHECKING:
    from flext_tests._constants.data_cases import (
        FlextTestsConstantsDataCases as FlextTestsConstantsDataCases,
    )
    from flext_tests._constants.docker import (
        FlextTestsConstantsDocker as FlextTestsConstantsDocker,
    )
    from flext_tests._constants.files import (
        FlextTestsConstantsFiles as FlextTestsConstantsFiles,
    )
    from flext_tests._constants.make import (
        FlextTestsConstantsMake as FlextTestsConstantsMake,
    )
    from flext_tests._constants.matcher import (
        FlextTestsConstantsMatcher as FlextTestsConstantsMatcher,
    )
    from flext_tests._constants.validator import (
        FlextTestsConstantsValidator as FlextTestsConstantsValidator,
    )

    # mro-i6nq.10: Static declaration mirrors the installer-owned runtime binding.
    __all__: tuple[str, ...]


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)


# mro-i6nq.10: The installer publishes __all__ from the manifest's literal ABI.
install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=_PUBLIC_EXPORTS)
