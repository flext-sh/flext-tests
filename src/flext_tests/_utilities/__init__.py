# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._files",
        "._make_parts",
        "._matchers",
    ),
    build_lazy_import_map(
        {
            "._files": ("_files",),
            "._files._assertions": ("FlextTestsFilesAssertionsMixin",),
            "._files._batch": ("FlextTestsFilesBatchMixin",),
            "._files._comparison_parts.comparison_part_02": (
                "FlextTestsFilesComparisonMixin",
            ),
            "._files._contexts": ("FlextTestsFilesContextsMixin",),
            "._files._creation_parts.creation_part_03": (
                "FlextTestsFilesCreationMixin",
            ),
            "._files._info": ("FlextTestsFilesInfoMixin",),
            "._files._lifecycle": ("FlextTestsFilesLifecycleMixin",),
            "._files._reading": ("FlextTestsFilesReadingMixin",),
            "._make_parts": ("_make_parts",),
            "._make_parts.make_contract_part_02": (
                "FlextTestsMakeContractUtilitiesMixin",
            ),
            "._make_parts.make_parsing_part_02": (
                "FlextTestsMakeParsingUtilitiesMixin",
            ),
            "._make_parts.make_registry_part_03": (
                "FlextTestsMakeRegistryUtilitiesMixin",
            ),
            "._make_parts.make_rendering_part_02": (
                "FlextTestsMakeRenderingUtilitiesMixin",
            ),
            "._matchers": ("_matchers",),
            "._matchers._assertions": ("FlextTestsMatchersAssertionsMixin",),
            "._matchers._containment": ("FlextTestsMatchersContainmentMixin",),
            "._matchers._result_parts.result_part_03": (
                "FlextTestsMatchersResultMixin",
            ),
            "._matchers._rules": ("FlextTestsMatchersRulesMixin",),
            "._matchers._scope": ("FlextTestsMatchersScopeMixin",),
            "._matchers._that_parts.that_part_06": ("FlextTestsMatchersThatMixin",),
            "._matchers._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
            ".container": ("FlextTestsContainerHelpersUtilitiesMixin",),
            ".files": ("FlextTestsFilesUtilitiesMixin",),
            ".fixtures_dsl": ("FlextTestsFixturesDSLMixin",),
            ".generic": ("FlextTestsGenericHelpersUtilitiesMixin",),
            ".handler": ("FlextTestsHandlerHelpersUtilitiesMixin",),
            ".make": ("FlextTestsMakeUtilitiesMixin",),
            ".matchers": (
                "FlextTestsMatchersUtilities",
                "tm",
            ),
            ".payload": ("FlextTestsPayloadUtilities",),
            ".result": ("FlextTestsResultUtilitiesMixin",),
            ".settings": ("FlextTestsConfigHelpersUtilitiesMixin",),
            ".testcontext": ("FlextTestsTestContextUtilitiesMixin",),
            ".validator": ("FlextTestsValidatorUtilitiesMixin",),
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
