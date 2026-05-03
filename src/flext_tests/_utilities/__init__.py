# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

_LAZY_IMPORTS = merge_lazy_imports(
    ("._matchers",),
    build_lazy_import_map(
        {
            "._matchers._assertions": ("FlextTestsMatchersAssertionsMixin",),
            "._matchers._typeguards": ("FlextTestsMatchersTypeGuardsMixin",),
            ".badobjects": ("FlextTestsBadObjectsUtilitiesMixin",),
            ".constants": ("FlextTestsConstantsHelpersUtilitiesMixin",),
            ".container": ("FlextTestsContainerHelpersUtilitiesMixin",),
            ".context": ("FlextTestsContextHelpersUtilitiesMixin",),
            ".domain": ("FlextTestsDomainHelpersUtilitiesMixin",),
            ".exception": ("FlextTestsExceptionHelpersUtilitiesMixin",),
            ".files": ("FlextTestsFilesUtilitiesMixin",),
            ".fixtures_dsl": ("FlextTestsFixturesDSLMixin",),
            ".generic": ("FlextTestsGenericHelpersUtilitiesMixin",),
            ".handler": ("FlextTestsHandlerHelpersUtilitiesMixin",),
            ".matchers": (
                "FlextTestsMatchersUtilities",
                "tm",
            ),
            ".parser": ("FlextTestsParserHelpersUtilitiesMixin",),
            ".payload": ("FlextTestsPayloadUtilities",),
            ".result": ("FlextTestsResultUtilitiesMixin",),
            ".settings": ("FlextTestsConfigHelpersUtilitiesMixin",),
            ".testcontext": ("FlextTestsTestContextUtilitiesMixin",),
            ".validation": ("FlextTestsValidationUtilitiesMixin",),
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
