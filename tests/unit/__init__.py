# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_docker": (
            "TestContainerInfo",
            "TestContainerStatus",
            "TestFlextTestsDocker",
            "TestFlextTestsDockerWorkerId",
            "TestFlextTestsDockerWorkspaceRoot",
        ),
        ".test_domains": ("TestFlextTestsDomains",),
        ".test_enforcement_dispatcher": (
            "TestActiveRules",
            "TestAutoActivation",
            "TestCsvSplit",
            "TestPublicHookSurface",
            "TestWorkspaceDiscovery",
        ),
        ".test_files": (
            "TestAssertExists",
            "TestBatchOperations",
            "TestCreateInStatic",
            "TestFileInfo",
            "TestFileInfoFromModels",
            "TestFlextTestsFiles",
            "TestFlextTestsFilesNewApi",
            "TestInfoWithContentMeta",
            "TestShortAlias",
        ),
        ".test_matchers": ("TestFlextTestsMatchers",),
        ".test_utilities": (
            "TestFlextTestsUtilitiesParser",
            "TestFlextTestsUtilitiesResult",
            "TestFlextTestsUtilitiesResultCompat",
            "TestFlextTestsUtilitiesTestContext",
        ),
        ".test_validator_types": ("TestFlextTestsValidatorTypes",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
