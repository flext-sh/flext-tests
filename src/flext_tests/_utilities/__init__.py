# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Utilities package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

# mro-i6nq.10: The package consumes its manifest's public-export contract.
from flext_tests._utilities.__unit__ import (
    CHILD_MODULE_PATHS as _CHILD_MODULE_PATHS,
    EXCLUDED_LAZY_NAMES as _EXCLUDED_LAZY_NAMES,
    LAZY_ALIAS_GROUPS as _LAZY_ALIAS_GROUPS,
    LAZY_MODULES as _LAZY_MODULES,
    PUBLIC_EXPORTS as _PUBLIC_EXPORTS,
)

if TYPE_CHECKING:
    from flext_tests._utilities import _files as _files, _matchers as _matchers
    from flext_tests._utilities.container import (
        FlextTestsContainerHelpersUtilitiesMixin as FlextTestsContainerHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.files import (
        FlextTestsFilesUtilitiesMixin as FlextTestsFilesUtilitiesMixin,
    )
    from flext_tests._utilities.generic import (
        FlextTestsGenericHelpersUtilitiesMixin as FlextTestsGenericHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.handler import (
        FlextTestsHandlerHelpersUtilitiesMixin as FlextTestsHandlerHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.make import (
        FlextTestsMakeUtilitiesMixin as FlextTestsMakeUtilitiesMixin,
    )
    from flext_tests._utilities.make_contract import (
        FlextTestsMakeContractUtilitiesMixin as FlextTestsMakeContractUtilitiesMixin,
    )
    from flext_tests._utilities.make_parsing import (
        FlextTestsMakeParsingUtilitiesMixin as FlextTestsMakeParsingUtilitiesMixin,
    )
    from flext_tests._utilities.make_registry import (
        FlextTestsMakeRegistryUtilitiesMixin as FlextTestsMakeRegistryUtilitiesMixin,
    )
    from flext_tests._utilities.make_rendering import (
        FlextTestsMakeRenderingUtilitiesMixin as FlextTestsMakeRenderingUtilitiesMixin,
    )
    from flext_tests._utilities.matchers import (
        FlextTestsMatchersUtilities as FlextTestsMatchersUtilities,
        tm as tm,
    )
    from flext_tests._utilities.payload import (
        FlextTestsPayloadUtilities as FlextTestsPayloadUtilities,
    )
    from flext_tests._utilities.result import (
        FlextTestsResultUtilitiesMixin as FlextTestsResultUtilitiesMixin,
    )
    from flext_tests._utilities.settings import (
        FlextTestsConfigHelpersUtilitiesMixin as FlextTestsConfigHelpersUtilitiesMixin,
    )
    from flext_tests._utilities.testcontext import (
        FlextTestsTestContextUtilitiesMixin as FlextTestsTestContextUtilitiesMixin,
    )
    from flext_tests._utilities.validator import (
        FlextTestsValidatorUtilitiesMixin as FlextTestsValidatorUtilitiesMixin,
    )

    # mro-i6nq.10: Static declaration mirrors the installer-owned runtime binding.
    __all__: tuple[str, ...]


_LAZY_IMPORTS = merge_lazy_imports(
    _CHILD_MODULE_PATHS,
    build_lazy_import_map(
        _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
    ),
    exclude_names=_EXCLUDED_LAZY_NAMES,
    module_name=__name__,
)


# mro-i6nq.10: The installer publishes __all__ from the manifest's literal ABI.
install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=_PUBLIC_EXPORTS)
