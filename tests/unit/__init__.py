# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_docker": ("TestsFlextTestsDocker",),
        ".test_domains": ("TestFlextTestsDomains",),
        ".test_enforcement_dispatcher": ("TestsFlextTestsEnforcementDispatcher",),
        ".test_files": ("TestsFlextTestsFiles",),
        ".test_matchers": ("TestFlextTestsMatchers",),
        ".test_utilities": ("TestsFlextTestsUtilitiesUnit",),
        ".test_validator_types": ("TestsFlextTestsValidatorTypes",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
