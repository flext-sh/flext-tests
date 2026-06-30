# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

TESTS_FLEXT_TESTS_LAZY_IMPORTS_PART_02 = build_lazy_import_map(
    {
        ".conftest": ("conftest",),
        ".constants": ("c",),
        ".integration": ("integration",),
        ".models": ("m",),
        ".protocols": ("p",),
        ".typings": ("t",),
        ".unit": ("unit",),
        ".unit.test_matchers": (
            "greater_than_two",
            "greater_than_zero",
            "is_negative",
            "is_positive",
            "is_string",
            "is_string_or_bytes",
        ),
        ".unit.test_utilities": ("TestsFlextTestsUtilitiesUnit",),
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

__all__: list[str] = ["TESTS_FLEXT_TESTS_LAZY_IMPORTS_PART_02"]
