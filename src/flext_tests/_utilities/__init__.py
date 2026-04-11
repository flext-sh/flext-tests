# AUTO-GENERATED FILE — Regenerate with: make gen
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".assertions": ("FlextTestsAssertionsUtilitiesMixin",),
        ".badobjects": ("FlextTestsBadObjectsUtilitiesMixin",),
        ".constants": ("FlextTestsConstantsHelpersUtilitiesMixin",),
        ".container": ("FlextTestsContainerHelpersUtilitiesMixin",),
        ".context": ("FlextTestsContextHelpersUtilitiesMixin",),
        ".deepmatch": ("FlextTestsDeepMatchUtilitiesMixin",),
        ".domain": ("FlextTestsDomainHelpersUtilitiesMixin",),
        ".exception": ("FlextTestsExceptionHelpersUtilitiesMixin",),
        ".factory": ("FlextTestsFactoryUtilitiesMixin",),
        ".files": ("FlextTestsFilesUtilitiesMixin",),
        ".generic": ("FlextTestsGenericHelpersUtilitiesMixin",),
        ".handler": ("FlextTestsHandlerHelpersUtilitiesMixin",),
        ".length": ("FlextTestsLengthUtilitiesMixin",),
        ".matchers": (
            "FlextTestsMatchersUtilities",
            "tm",
        ),
        ".parser": ("FlextTestsParserHelpersUtilitiesMixin",),
        ".payload": ("FlextTestsPayloadUtilities",),
        ".registry": ("FlextTestsRegistryHelpersUtilitiesMixin",),
        ".result": ("FlextTestsResultUtilitiesMixin",),
        ".settings": ("FlextTestsConfigHelpersUtilitiesMixin",),
        ".testcase": ("FlextTestsTestCaseHelpersUtilitiesMixin",),
        ".testcontext": ("FlextTestsTestContextUtilitiesMixin",),
        ".validation": ("FlextTestsValidationUtilitiesMixin",),
        ".validator": ("FlextTestsValidatorUtilitiesMixin",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
