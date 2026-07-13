# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

# mro-i6nq.10: The package consumes its manifest's public-export contract.
from flext_tests.__unit__ import (
    LAZY_ALIAS_GROUPS as _LAZY_ALIAS_GROUPS,
    LAZY_MODULES as _LAZY_MODULES,
    PUBLIC_EXPORTS as _PUBLIC_EXPORTS,
)
from flext_tests.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_infra import d as d, e as e, h as h, r as r, x as x
    from flext_tests._config import (
        FlextTestsConfig as FlextTestsConfig,
        config as config,
    )
    from flext_tests._settings import (
        FlextTestsSettings as FlextTestsSettings,
        settings as settings,
    )
    from flext_tests.base import (
        FlextTestsCase as FlextTestsCase,
        FlextTestsServiceBase as FlextTestsServiceBase,
        s as s,
    )
    from flext_tests.constants import FlextTestsConstants as FlextTestsConstants, c as c
    from flext_tests.docker import FlextTestsDocker as FlextTestsDocker, tk as tk
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
