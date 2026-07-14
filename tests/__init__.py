# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests import (
        d as d,
        e as e,
        h as h,
        r as r,
        s as s,
        td as td,
        tf as tf,
        tk as tk,
        tm as tm,
        tv as tv,
        x as x,
    )
    from tests.constants import (
        TestsFlextTestsConstants as TestsFlextTestsConstants,
        c as c,
    )
    from tests.integration.test_docker_integration import (
        TestsFlextTestsDockerIntegration as TestsFlextTestsDockerIntegration,
    )
    from tests.models import TestsFlextTestsModels as TestsFlextTestsModels, m as m
    from tests.protocols import (
        TestsFlextTestsProtocols as TestsFlextTestsProtocols,
        p as p,
    )
    from tests.typings import TestsFlextTestsTypes as TestsFlextTestsTypes, t as t
    from tests.unit._docker_parts.builders import (
        DockerBuildersMixin as DockerBuildersMixin,
    )
    from tests.unit._docker_parts.operations import (
        DockerOperationsMixin as DockerOperationsMixin,
    )
    from tests.unit._docker_parts.state import DockerStateMixin as DockerStateMixin
    from tests.unit._docker_parts.targets import (
        DockerTargetsMixin as DockerTargetsMixin,
    )
    from tests.unit._files_parts.assert_exists import (
        FilesAssertExistsMixin as FilesAssertExistsMixin,
    )
    from tests.unit._files_parts.batch_create_in import (
        FilesBatchCreateInMixin as FilesBatchCreateInMixin,
    )
    from tests.unit._files_parts.compare import FilesCompareMixin as FilesCompareMixin
    from tests.unit._files_parts.content_meta import (
        FilesContentMetaMixin as FilesContentMetaMixin,
    )
    from tests.unit._files_parts.contexts import (
        FilesContextsMixin as FilesContextsMixin,
    )
    from tests.unit._files_parts.creation import (
        FilesCreationMixin as FilesCreationMixin,
    )
    from tests.unit._files_parts.formats import FilesFormatsMixin as FilesFormatsMixin
    from tests.unit._files_parts.info_cleanup import (
        FilesInfoCleanupMixin as FilesInfoCleanupMixin,
    )
    from tests.unit._files_parts.info_metadata import (
        FilesInfoMetadataMixin as FilesInfoMetadataMixin,
    )
    from tests.unit._files_parts.models import FilesModelsMixin as FilesModelsMixin
    from tests.unit._files_parts.read import FilesReadMixin as FilesReadMixin
    from tests.unit._matchers_parts.data_driven import (
        MatchersDataDrivenMixin as MatchersDataDrivenMixin,
    )
    from tests.unit._matchers_parts.fail_constraints import (
        MatchersFailConstraintsMixin as MatchersFailConstraintsMixin,
    )
    from tests.unit._matchers_parts.ok_constraints import (
        MatchersOkConstraintsMixin as MatchersOkConstraintsMixin,
    )
    from tests.unit._matchers_parts.predicates import (
        MatchersPredicates as MatchersPredicates,
    )
    from tests.unit._matchers_parts.results import (
        MatchersResultsMixin as MatchersResultsMixin,
    )
    from tests.unit._matchers_parts.scope_errors import (
        MatchersScopeErrorsMixin as MatchersScopeErrorsMixin,
    )
    from tests.unit._matchers_parts.that_attrs import (
        MatchersThatAttrsMixin as MatchersThatAttrsMixin,
    )
    from tests.unit._matchers_parts.that_collections import (
        MatchersThatCollectionsMixin as MatchersThatCollectionsMixin,
    )
    from tests.unit._matchers_parts.validation import (
        MatchersValidationMixin as MatchersValidationMixin,
    )
    from tests.unit.test_docker import TestsFlextTestsDocker as TestsFlextTestsDocker
    from tests.unit.test_domains import TestsFlextTestsDomains as TestsFlextTestsDomains
    from tests.unit.test_enforcement_dispatcher import (
        TestsFlextTestsEnforcementDispatcher as TestsFlextTestsEnforcementDispatcher,
    )
    from tests.unit.test_enforcement_plugin import (
        TestsFlextTestsEnforcementPlugin as TestsFlextTestsEnforcementPlugin,
    )
    from tests.unit.test_files import TestsFlextTestsFiles as TestsFlextTestsFiles
    from tests.unit.test_matchers import (
        TestsFlextTestsMatchers as TestsFlextTestsMatchers,
    )
    from tests.unit.test_validator_imports_bypass import (
        TestsFlextTestsValidatorImportsBypass as TestsFlextTestsValidatorImportsBypass,
    )
    from tests.unit.test_validator_layer_tests_markdown import (
        TestsFlextTestsValidatorLayerTestsMarkdown as TestsFlextTestsValidatorLayerTestsMarkdown,
    )
    from tests.unit.test_validator_types import (
        TestsFlextTestsValidatorTypes as TestsFlextTestsValidatorTypes,
    )
    from tests.utilities import (
        TestsFlextTestsUtilities as TestsFlextTestsUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (".integration", ".unit"),
    build_lazy_import_map({
        ".conftest": ("conftest",),
        ".constants": ("TestsFlextTestsConstants", "c"),
        ".integration": ("integration",),
        ".integration.test_docker_integration": ("TestsFlextTestsDockerIntegration",),
        ".models": ("TestsFlextTestsModels", "m"),
        ".protocols": ("TestsFlextTestsProtocols", "p"),
        ".typings": ("TestsFlextTestsTypes", "t"),
        ".unit": ("unit",),
        ".unit._docker_parts.builders": ("DockerBuildersMixin",),
        ".unit._docker_parts.operations": ("DockerOperationsMixin",),
        ".unit._docker_parts.state": ("DockerStateMixin",),
        ".unit._docker_parts.targets": ("DockerTargetsMixin",),
        ".unit._files_parts.assert_exists": ("FilesAssertExistsMixin",),
        ".unit._files_parts.batch_create_in": ("FilesBatchCreateInMixin",),
        ".unit._files_parts.compare": ("FilesCompareMixin",),
        ".unit._files_parts.content_meta": ("FilesContentMetaMixin",),
        ".unit._files_parts.contexts": ("FilesContextsMixin",),
        ".unit._files_parts.creation": ("FilesCreationMixin",),
        ".unit._files_parts.formats": ("FilesFormatsMixin",),
        ".unit._files_parts.info_cleanup": ("FilesInfoCleanupMixin",),
        ".unit._files_parts.info_metadata": ("FilesInfoMetadataMixin",),
        ".unit._files_parts.models": ("FilesModelsMixin",),
        ".unit._files_parts.read": ("FilesReadMixin",),
        ".unit._matchers_parts.data_driven": ("MatchersDataDrivenMixin",),
        ".unit._matchers_parts.fail_constraints": ("MatchersFailConstraintsMixin",),
        ".unit._matchers_parts.ok_constraints": ("MatchersOkConstraintsMixin",),
        ".unit._matchers_parts.predicates": ("MatchersPredicates",),
        ".unit._matchers_parts.results": ("MatchersResultsMixin",),
        ".unit._matchers_parts.scope_errors": ("MatchersScopeErrorsMixin",),
        ".unit._matchers_parts.that_attrs": ("MatchersThatAttrsMixin",),
        ".unit._matchers_parts.that_collections": ("MatchersThatCollectionsMixin",),
        ".unit._matchers_parts.validation": ("MatchersValidationMixin",),
        ".unit.test_docker": ("TestsFlextTestsDocker",),
        ".unit.test_domains": ("TestsFlextTestsDomains",),
        ".unit.test_enforcement_dispatcher": ("TestsFlextTestsEnforcementDispatcher",),
        ".unit.test_enforcement_plugin": ("TestsFlextTestsEnforcementPlugin",),
        ".unit.test_files": ("TestsFlextTestsFiles",),
        ".unit.test_matchers": ("TestsFlextTestsMatchers",),
        ".unit.test_validator_imports_bypass": (
            "TestsFlextTestsValidatorImportsBypass",
        ),
        ".unit.test_validator_layer_tests_markdown": (
            "TestsFlextTestsValidatorLayerTestsMarkdown",
        ),
        ".unit.test_validator_types": ("TestsFlextTestsValidatorTypes",),
        ".utilities": ("TestsFlextTestsUtilities", "u"),
        "flext_tests": ("d", "e", "h", "r", "s", "td", "tf", "tk", "tm", "tv", "x"),
    }),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
