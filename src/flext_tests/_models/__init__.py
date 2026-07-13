# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

# mro-i6nq.10: The package consumes its manifest's public-export contract.
from flext_tests._models.__unit__ import (
    CHILD_MODULE_PATHS as _CHILD_MODULE_PATHS,
    EXCLUDED_LAZY_NAMES as _EXCLUDED_LAZY_NAMES,
    LAZY_ALIAS_GROUPS as _LAZY_ALIAS_GROUPS,
    LAZY_MODULES as _LAZY_MODULES,
    PUBLIC_EXPORTS as _PUBLIC_EXPORTS,
)

if TYPE_CHECKING:
    from flext_tests._models import (
        _filesystem_parts as _filesystem_parts,
        _matchers_parts as _matchers_parts,
    )
    from flext_tests._models._filesystem_parts.filesystem_part_02 import (
        FlextTestsFilesystemModelsMixin as FlextTestsFilesystemModelsMixin,
    )
    from flext_tests._models._matchers_parts.matchers_part_03 import (
        FlextTestsMatchersModelsMixin as FlextTestsMatchersModelsMixin,
    )
    from flext_tests._models.base import (
        FlextTestsBaseModelsMixin as FlextTestsBaseModelsMixin,
    )
    from flext_tests._models.batch import (
        FlextTestsBatchModelsMixin as FlextTestsBatchModelsMixin,
    )
    from flext_tests._models.docker import (
        FlextTestsDockerModelsMixin as FlextTestsDockerModelsMixin,
    )
    from flext_tests._models.domains import (
        FlextTestsDomainModelsMixin as FlextTestsDomainModelsMixin,
    )
    from flext_tests._models.make import (
        FlextTestsMakeModelsMixin as FlextTestsMakeModelsMixin,
    )
    from flext_tests._models.validator import (
        FlextTestsValidatorModelsMixin as FlextTestsValidatorModelsMixin,
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
