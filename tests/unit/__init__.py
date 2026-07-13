# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
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
            "._matchers_parts.predicates": ("MatchersPredicates",),
            "._matchers_parts.results": ("MatchersResultsMixin",),
            "._matchers_parts.scope_errors": ("MatchersScopeErrorsMixin",),
            "._matchers_parts.that_attrs": ("MatchersThatAttrsMixin",),
            "._matchers_parts.that_collections": ("MatchersThatCollectionsMixin",),
            "._matchers_parts.validation": ("MatchersValidationMixin",),
            ".test_docker": ("TestsFlextTestsDocker",),
            ".test_domains": ("TestsFlextTestsDomains",),
            ".test_enforcement_dispatcher": ("TestsFlextTestsEnforcementDispatcher",),
            ".test_enforcement_plugin": ("TestsFlextTestsEnforcementPlugin",),
            ".test_files": ("TestsFlextTestsFiles",),
            ".test_matchers": ("TestsFlextTestsMatchers",),
            ".test_utilities": ("TestsFlextTestsUtilities",),
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
