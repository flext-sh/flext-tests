# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
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
    from flext_cli import c as cli_c, d, e, h, r, x
    from flext_infra import c as infra_c

    from . import services
    from .__version__ import FlextTestsVersion
    from ._config import FlextTestsConfig, config
    from ._settings import FlextTestsSettings, settings
    from .api import FlextTests, api
    from .base import FlextTestsServiceBase, FlextTestsServiceBase as s
    from .case import FlextTestsCase
    from .cli import FlextTestsCli
    from .constants import FlextTestsConstants, FlextTestsConstants as c
    from .docker import FlextTestsDocker, tk
    from .domains import FlextTestsDomains, td
    from .enforcement import (
        FlextTestsEnforcementCollector,
        FlextTestsEnforcementItem,
        FlextTestsEnforcementViolationError,
        active_rules,
        discover_repository_root,
        load_infra_report,
        split_csv,
    )
    from .enforcement_plugin import SLOW_TIMEOUT_INI_OPTION
    from .files import FlextTestsFiles, tf
    from .kube import FlextTestsKube
    from .models import FlextTestsModels, FlextTestsModels as m
    from .protocols import FlextTestsProtocols, FlextTestsProtocols as p
    from .pytest_bootstrap import install_local_packages
    from .tmatchers import FlextTestsMatchersUtilities, tm
    from .typings import FlextTestsTypes, FlextTestsTypes as t
    from .utilities import (
        FlextTestsFixturesDSLMixin,
        FlextTestsModuleGovernanceMixin,
        FlextTestsUtilities,
        FlextTestsUtilities as u,
    )
    from .validator import FlextTestsValidator, tv
__all__: tuple[str, ...] = (
    "SLOW_TIMEOUT_INI_OPTION",
    "FlextTests",
    "FlextTestsCase",
    "FlextTestsCli",
    "FlextTestsConfig",
    "FlextTestsConstants",
    "FlextTestsDocker",
    "FlextTestsDomains",
    "FlextTestsEnforcementCollector",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementViolationError",
    "FlextTestsFiles",
    "FlextTestsFixturesDSLMixin",
    "FlextTestsKube",
    "FlextTestsMatchersUtilities",
    "FlextTestsModels",
    "FlextTestsModuleGovernanceMixin",
    "FlextTestsProtocols",
    "FlextTestsServiceBase",
    "FlextTestsSettings",
    "FlextTestsTypes",
    "FlextTestsUtilities",
    "FlextTestsValidator",
    "FlextTestsVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "active_rules",
    "api",
    "c",
    "cli_c",
    "config",
    "d",
    "discover_repository_root",
    "e",
    "h",
    "infra_c",
    "install_local_packages",
    "load_infra_report",
    "m",
    "p",
    "r",
    "s",
    "services",
    "settings",
    "split_csv",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".__version__": ("FlextTestsVersion",),
            "._config": ("FlextTestsConfig", "config"),
            "._settings": ("FlextTestsSettings", "settings"),
            ".api": ("FlextTests", "api"),
            ".base": ("FlextTestsServiceBase", "s"),
            ".case": ("FlextTestsCase",),
            ".cli": ("FlextTestsCli",),
            ".constants": ("FlextTestsConstants", "c"),
            ".docker": ("FlextTestsDocker", "tk"),
            ".domains": ("FlextTestsDomains", "td"),
            ".enforcement": (
                "FlextTestsEnforcementCollector",
                "FlextTestsEnforcementItem",
                "FlextTestsEnforcementViolationError",
                "active_rules",
                "discover_repository_root",
                "load_infra_report",
                "split_csv",
            ),
            ".enforcement_plugin": ("SLOW_TIMEOUT_INI_OPTION",),
            ".files": ("FlextTestsFiles", "tf"),
            ".kube": ("FlextTestsKube",),
            ".models": ("FlextTestsModels", "m"),
            ".protocols": ("FlextTestsProtocols", "p"),
            ".pytest_bootstrap": ("install_local_packages",),
            ".services": ("services",),
            ".tmatchers": ("FlextTestsMatchersUtilities", "tm"),
            ".typings": ("FlextTestsTypes", "t"),
            ".utilities": (
                "FlextTestsFixturesDSLMixin",
                "FlextTestsModuleGovernanceMixin",
                "FlextTestsUtilities",
                "u",
            ),
            ".validator": ("FlextTestsValidator", "tv"),
            "flext_cli": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({
            "flext_cli": (("cli_c", "c"),),
            "flext_infra": (("infra_c", "c"),),
        }),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
