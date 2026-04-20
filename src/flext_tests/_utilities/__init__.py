# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".badobjects": ("FlextTestsBadObjectsUtilitiesMixin",),
        ".constants": ("FlextTestsConstantsHelpersUtilitiesMixin",),
        ".container": ("FlextTestsContainerHelpersUtilitiesMixin",),
        ".context": ("FlextTestsContextHelpersUtilitiesMixin",),
        ".domain": ("FlextTestsDomainHelpersUtilitiesMixin",),
        ".exception": ("FlextTestsExceptionHelpersUtilitiesMixin",),
        ".files": ("FlextTestsFilesUtilitiesMixin",),
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
        ".testcase": ("FlextTestsTestCaseHelpersUtilitiesMixin",),
        ".testcontext": ("FlextTestsTestContextUtilitiesMixin",),
        ".validation": ("FlextTestsValidationUtilitiesMixin",),
        ".validator": ("FlextTestsValidatorUtilitiesMixin",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
