# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import _docker_parts as _docker_parts
    from . import _files_parts as _files_parts
    from . import _matchers_parts as _matchers_parts
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from ._docker_parts.builders import DockerBuildersMixin
    from ._docker_parts.operations import DockerOperationsMixin
    from ._docker_parts.state import DockerStateMixin
    from ._docker_parts.targets import DockerTargetsMixin
    from ._files_parts.assert_exists import FilesAssertExistsMixin
    from ._files_parts.batch_create_in import FilesBatchCreateInMixin
    from ._files_parts.compare import FilesCompareMixin
    from ._files_parts.content_meta import FilesContentMetaMixin
    from ._files_parts.contexts import FilesContextsMixin
    from ._files_parts.creation import FilesCreationMixin
    from ._files_parts.formats import FilesFormatsMixin
    from ._files_parts.info_cleanup import FilesInfoCleanupMixin
    from ._files_parts.info_metadata import FilesInfoMetadataMixin
    from ._files_parts.models import FilesModelsMixin
    from ._files_parts.read import FilesReadMixin
    from ._matchers_parts.data_driven import MatchersDataDrivenMixin
    from ._matchers_parts.fail_constraints import MatchersFailConstraintsMixin
    from ._matchers_parts.ok_constraints import MatchersOkConstraintsMixin
    from ._matchers_parts.predicates import MatchersPredicates
    from ._matchers_parts.rejects_assignment import MatchersRejectsAssignmentMixin
    from ._matchers_parts.results import MatchersResultsMixin
    from ._matchers_parts.scope_errors import MatchersScopeErrorsMixin
    from ._matchers_parts.that_attrs import MatchersThatAttrsMixin
    from ._matchers_parts.that_collections import MatchersThatCollectionsMixin
    from ._matchers_parts.validation import MatchersValidationMixin
    from .test_docker import TestsFlextTestsDocker, docker_manager
    from .test_domains import TestsFlextTestsDomains
    from .test_enforcement_dispatcher import TestsFlextTestsEnforcementDispatcher
    from .test_enforcement_plugin import TestsFlextTestsEnforcementPlugin
    from .test_enforcement_slow_timeout import TestsFlextTestsSlowTimeoutPolicy
    from .test_files import TestsFlextTestsFiles
    from .test_matchers import TestsFlextTestsMatchers
    from .test_public_facade import TestsFlextTestsPublicFacade
    from .test_utilities import TestsFlextTestsUtilities
    from .test_validator_imports_bypass import TestsFlextTestsValidatorImportsBypass
    from .test_validator_layer_tests_markdown import (
        TestsFlextTestsValidatorLayerTestsMarkdown,
    )
    from .test_validator_types import TestsFlextTestsValidatorTypes
    from .test_workspace_cleanup import TestsFlextTestsWorkspaceCleanup
__all__: tuple[str, ...] = (
    "DockerBuildersMixin",
    "DockerOperationsMixin",
    "DockerStateMixin",
    "DockerTargetsMixin",
    "FilesAssertExistsMixin",
    "FilesBatchCreateInMixin",
    "FilesCompareMixin",
    "FilesContentMetaMixin",
    "FilesContextsMixin",
    "FilesCreationMixin",
    "FilesFormatsMixin",
    "FilesInfoCleanupMixin",
    "FilesInfoMetadataMixin",
    "FilesModelsMixin",
    "FilesReadMixin",
    "MatchersDataDrivenMixin",
    "MatchersFailConstraintsMixin",
    "MatchersOkConstraintsMixin",
    "MatchersPredicates",
    "MatchersRejectsAssignmentMixin",
    "MatchersResultsMixin",
    "MatchersScopeErrorsMixin",
    "MatchersThatAttrsMixin",
    "MatchersThatCollectionsMixin",
    "MatchersValidationMixin",
    "TestsFlextTestsDocker",
    "TestsFlextTestsDomains",
    "TestsFlextTestsEnforcementDispatcher",
    "TestsFlextTestsEnforcementPlugin",
    "TestsFlextTestsFiles",
    "TestsFlextTestsMatchers",
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
    "c",
    "d",
    "docker_manager",
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
            "._docker_parts.builders": ("DockerBuildersMixin",),
            "._docker_parts.operations": ("DockerOperationsMixin",),
            "._docker_parts.state": ("DockerStateMixin",),
            "._docker_parts.targets": ("DockerTargetsMixin",),
            "._files_parts": ("_files_parts",),
            "._files_parts.assert_exists": ("FilesAssertExistsMixin",),
            "._files_parts.batch_create_in": ("FilesBatchCreateInMixin",),
            "._files_parts.compare": ("FilesCompareMixin",),
            "._files_parts.content_meta": ("FilesContentMetaMixin",),
            "._files_parts.contexts": ("FilesContextsMixin",),
            "._files_parts.creation": ("FilesCreationMixin",),
            "._files_parts.formats": ("FilesFormatsMixin",),
            "._files_parts.info_cleanup": ("FilesInfoCleanupMixin",),
            "._files_parts.info_metadata": ("FilesInfoMetadataMixin",),
            "._files_parts.models": ("FilesModelsMixin",),
            "._files_parts.read": ("FilesReadMixin",),
            "._matchers_parts": ("_matchers_parts",),
            "._matchers_parts.data_driven": ("MatchersDataDrivenMixin",),
            "._matchers_parts.fail_constraints": ("MatchersFailConstraintsMixin",),
            "._matchers_parts.ok_constraints": ("MatchersOkConstraintsMixin",),
            "._matchers_parts.predicates": ("MatchersPredicates",),
            "._matchers_parts.rejects_assignment": ("MatchersRejectsAssignmentMixin",),
            "._matchers_parts.results": ("MatchersResultsMixin",),
            "._matchers_parts.scope_errors": ("MatchersScopeErrorsMixin",),
            "._matchers_parts.that_attrs": ("MatchersThatAttrsMixin",),
            "._matchers_parts.that_collections": ("MatchersThatCollectionsMixin",),
            "._matchers_parts.validation": ("MatchersValidationMixin",),
            ".test_docker": ("TestsFlextTestsDocker", "docker_manager"),
            ".test_domains": ("TestsFlextTestsDomains",),
            ".test_enforcement_dispatcher": ("TestsFlextTestsEnforcementDispatcher",),
            ".test_enforcement_plugin": ("TestsFlextTestsEnforcementPlugin",),
            ".test_enforcement_slow_timeout": ("TestsFlextTestsSlowTimeoutPolicy",),
            ".test_files": ("TestsFlextTestsFiles",),
            ".test_matchers": ("TestsFlextTestsMatchers",),
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
