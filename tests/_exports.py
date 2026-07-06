# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, merge_lazy_imports

_LOCAL_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".conftest": ("conftest",),
        ".constants": (
            "TestsFlextTestsConstants",
            "c",
        ),
        ".integration": ("integration",),
        ".integration.test_docker_integration": ("TestsFlextTestsDockerIntegration",),
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
)

TESTS_FLEXT_TESTS_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".integration",
        ".unit",
    ),
    _LOCAL_LAZY_IMPORTS,
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
    module_name="tests",
)

__all__: list[str] = ["TESTS_FLEXT_TESTS_LAZY_IMPORTS"]
