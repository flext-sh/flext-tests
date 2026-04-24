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
    from flext_tests import d, e, h, r, s, td, tf, tk, tm, tv, x
    from tests.constants import TestsFlextTestsConstants, c
    from tests.models import TestsFlextTestsModels, m
    from tests.protocols import TestsFlextTestsProtocols, p
    from tests.typings import TestsFlextTestsTypes, t
    from tests.unit.test_docker import TestsFlextTestsDocker
    from tests.unit.test_domains import TestFlextTestsDomains
    from tests.unit.test_enforcement_dispatcher import (
        TestsFlextTestsEnforcementDispatcher,
    )
    from tests.unit.test_files import TestsFlextTestsFiles
    from tests.unit.test_matchers import TestFlextTestsMatchers
    from tests.unit.test_utilities import TestsFlextTestsUtilitiesUnit
    from tests.unit.test_validator_types import TestsFlextTestsValidatorTypes
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
            ".unit.test_docker": ("TestsFlextTestsDocker",),
            ".unit.test_domains": ("TestFlextTestsDomains",),
            ".unit.test_enforcement_dispatcher": (
                "TestsFlextTestsEnforcementDispatcher",
            ),
            ".unit.test_files": ("TestsFlextTestsFiles",),
            ".unit.test_matchers": ("TestFlextTestsMatchers",),
            ".unit.test_utilities": ("TestsFlextTestsUtilitiesUnit",),
            ".unit.test_validator_types": ("TestsFlextTestsValidatorTypes",),
            ".utilities": (
                "TestsFlextTestsUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
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

__all__: list[str] = [
    "TestFlextTestsDomains",
    "TestFlextTestsMatchers",
    "TestsFlextTestsConstants",
    "TestsFlextTestsDocker",
    "TestsFlextTestsEnforcementDispatcher",
    "TestsFlextTestsFiles",
    "TestsFlextTestsModels",
    "TestsFlextTestsProtocols",
    "TestsFlextTestsTypes",
    "TestsFlextTestsUtilities",
    "TestsFlextTestsUtilitiesUnit",
    "TestsFlextTestsValidatorTypes",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
