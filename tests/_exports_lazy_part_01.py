# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

TESTS_FLEXT_TESTS_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        ".constants": ("TestsFlextTestsConstants",),
        ".integration.test_docker_integration": ("TestsFlextTestsDockerIntegration",),
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
    },
)

__all__: list[str] = ["TESTS_FLEXT_TESTS_LAZY_IMPORTS_PART_01"]
