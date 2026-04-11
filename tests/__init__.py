# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests._fixtures.settings import (
        reset_settings,
        settings,
        settings_factory,
    )
    from flext_tests._utilities.matchers import tm
    from flext_tests.docker import tk
    from flext_tests.domains import td
    from flext_tests.files import tf
    from flext_tests.validator import tv
    from tests.constants import TestsFlextTestsConstants, c
    from tests.models import TestsFlextTestsModels, m
    from tests.protocols import TestsFlextTestsProtocols, p
    from tests.typings import TestsFlextTestsTypes, t
    from tests.utilities import TestsFlextTestsUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".constants": (
                "TestsFlextTestsConstants",
                "c",
            ),
            ".models": (
                "TestsFlextTestsModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextTestsProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextTestsTypes",
                "t",
            ),
            ".utilities": (
                "TestsFlextTestsUtilities",
                "u",
            ),
            "flext_tests._fixtures.settings": (
                "reset_settings",
                "settings",
                "settings_factory",
            ),
            "flext_tests._utilities.matchers": ("tm",),
            "flext_tests.docker": ("tk",),
            "flext_tests.domains": ("td",),
            "flext_tests.files": ("tf",),
            "flext_tests.validator": ("tv",),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "TestsFlextTestsConstants",
    "TestsFlextTestsModels",
    "TestsFlextTestsProtocols",
    "TestsFlextTestsTypes",
    "TestsFlextTestsUtilities",
    "c",
    "m",
    "p",
    "reset_settings",
    "settings",
    "settings_factory",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
]
