# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

# mro-i6nq.10: The package consumes its manifest's public-export contract.
from flext_tests._models.__unit__ import (
    LAZY_ALIAS_GROUPS as _LAZY_ALIAS_GROUPS,
    LAZY_MODULES as _LAZY_MODULES,
    PUBLIC_EXPORTS as _PUBLIC_EXPORTS,
)

if TYPE_CHECKING:
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
    from flext_tests._models.filesystem import (
        FlextTestsFilesystemModelsMixin as FlextTestsFilesystemModelsMixin,
    )
    from flext_tests._models.make import (
        FlextTestsMakeModelsMixin as FlextTestsMakeModelsMixin,
    )
    from flext_tests._models.matchers import (
        FlextTestsMatchersModelsMixin as FlextTestsMatchersModelsMixin,
    )
    from flext_tests._models.validator import (
        FlextTestsValidatorModelsMixin as FlextTestsValidatorModelsMixin,
    )

    # mro-i6nq.10: Static declaration mirrors the installer-owned runtime binding.
    __all__: tuple[str, ...]


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)


# mro-i6nq.10: The installer publishes __all__ from the manifest's literal ABI.
install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=_PUBLIC_EXPORTS)
