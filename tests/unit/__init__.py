# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_tests import (
        c as c,
        d as d,
        e as e,
        h as h,
        m as m,
        p as p,
        r as r,
        s as s,
        t as t,
        td as td,
        tf as tf,
        tk as tk,
        tm as tm,
        tv as tv,
        u as u,
        x as x,
    )
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
    from tests.unit.test_files import TestsFlextTestsFiles as TestsFlextTestsFiles
    from tests.unit.test_matchers import (
        TestsFlextTestsMatchers as TestsFlextTestsMatchers,
        greater_than_two as greater_than_two,
        greater_than_zero as greater_than_zero,
        is_negative as is_negative,
        is_positive as is_positive,
        is_string as is_string,
        is_string_or_bytes as is_string_or_bytes,
    )
    from tests.unit.test_utilities import (
        TestsFlextTestsUtilitiesUnit as TestsFlextTestsUtilitiesUnit,
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
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._docker_parts",
        "._files_parts",
        "._matchers_parts",
    ),
    build_lazy_import_map(
        {
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
            "._matchers_parts.results": ("MatchersResultsMixin",),
            "._matchers_parts.scope_errors": ("MatchersScopeErrorsMixin",),
            "._matchers_parts.that_attrs": ("MatchersThatAttrsMixin",),
            "._matchers_parts.that_collections": ("MatchersThatCollectionsMixin",),
            "._matchers_parts.validation": ("MatchersValidationMixin",),
            ".test_docker": ("TestsFlextTestsDocker",),
            ".test_domains": ("TestsFlextTestsDomains",),
            ".test_enforcement_dispatcher": ("TestsFlextTestsEnforcementDispatcher",),
            ".test_files": ("TestsFlextTestsFiles",),
            ".test_matchers": (
                "TestsFlextTestsMatchers",
                "greater_than_two",
                "greater_than_zero",
                "is_negative",
                "is_positive",
                "is_string",
                "is_string_or_bytes",
            ),
            ".test_utilities": ("TestsFlextTestsUtilitiesUnit",),
            ".test_validator_imports_bypass": (
                "TestsFlextTestsValidatorImportsBypass",
            ),
            ".test_validator_layer_tests_markdown": (
                "TestsFlextTestsValidatorLayerTestsMarkdown",
            ),
            ".test_validator_types": ("TestsFlextTestsValidatorTypes",),
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
