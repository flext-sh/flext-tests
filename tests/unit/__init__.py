# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from . import _docker_parts, _files_parts, _matchers_parts, _validator_parts
    from .test_docker import TestsFlextTestsDocker
    from .test_domains import TestsFlextTestsDomains
    from .test_enforcement_dispatcher import TestsFlextTestsEnforcementDispatcher
    from .test_enforcement_plugin import TestsFlextTestsEnforcementPlugin
    from .test_enforcement_slow_timeout import TestsFlextTestsSlowTimeoutPolicy
    from .test_files import TestsFlextTestsFiles
    from .test_matchers import TestsFlextTestsMatchers
    from .test_mypy_matcher_repro import TestsFlextTestsMypyMatcherRepro
    from .test_payload import TestsFlextTestsPayload
    from .test_public_facade import TestsFlextTestsPublicFacade
    from .test_utilities import TestsFlextTestsUtilities
    from .test_validator_imports_bypass import TestsFlextTestsValidatorImportsBypass
    from .test_validator_layer_tests_markdown import (
        TestsFlextTestsValidatorLayerTestsMarkdown,
    )
    from .test_validator_types import TestsFlextTestsValidatorTypes
    from .test_workspace_cleanup import TestsFlextTestsWorkspaceCleanup
__all__: tuple[str, ...] = (
    "TestsFlextTestsDocker",
    "TestsFlextTestsDomains",
    "TestsFlextTestsEnforcementDispatcher",
    "TestsFlextTestsEnforcementPlugin",
    "TestsFlextTestsFiles",
    "TestsFlextTestsMatchers",
    "TestsFlextTestsMypyMatcherRepro",
    "TestsFlextTestsPayload",
    "TestsFlextTestsPublicFacade",
    "TestsFlextTestsSlowTimeoutPolicy",
    "TestsFlextTestsUtilities",
    "TestsFlextTestsValidatorImportsBypass",
    "TestsFlextTestsValidatorLayerTestsMarkdown",
    "TestsFlextTestsValidatorTypes",
    "TestsFlextTestsWorkspaceCleanup",
    "_docker_parts",
    "_files_parts",
    "_matchers_parts",
    "_validator_parts",
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
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._docker_parts": ("_docker_parts",),
            "._files_parts": ("_files_parts",),
            "._matchers_parts": ("_matchers_parts",),
            "._validator_parts": ("_validator_parts",),
            ".test_docker": ("TestsFlextTestsDocker",),
            ".test_domains": ("TestsFlextTestsDomains",),
            ".test_enforcement_dispatcher": ("TestsFlextTestsEnforcementDispatcher",),
            ".test_enforcement_plugin": ("TestsFlextTestsEnforcementPlugin",),
            ".test_enforcement_slow_timeout": ("TestsFlextTestsSlowTimeoutPolicy",),
            ".test_files": ("TestsFlextTestsFiles",),
            ".test_matchers": ("TestsFlextTestsMatchers",),
            ".test_mypy_matcher_repro": ("TestsFlextTestsMypyMatcherRepro",),
            ".test_payload": ("TestsFlextTestsPayload",),
            ".test_public_facade": ("TestsFlextTestsPublicFacade",),
            ".test_utilities": ("TestsFlextTestsUtilities",),
            ".test_validator_imports_bypass": (
                "TestsFlextTestsValidatorImportsBypass",
            ),
            ".test_validator_layer_tests_markdown": (
                "TestsFlextTestsValidatorLayerTestsMarkdown",
            ),
            ".test_validator_types": ("TestsFlextTestsValidatorTypes",),
            ".test_workspace_cleanup": ("TestsFlextTestsWorkspaceCleanup",),
            "flext_tests": (
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
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
