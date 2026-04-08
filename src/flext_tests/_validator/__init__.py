# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Validator package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextTestsValidatorModels": (
        "flext_tests._validator.models",
        "FlextTestsValidatorModels",
    ),
    "FlextValidatorBypass": ("flext_tests._validator.bypass", "FlextValidatorBypass"),
    "FlextValidatorImports": (
        "flext_tests._validator.imports",
        "FlextValidatorImports",
    ),
    "FlextValidatorLayer": ("flext_tests._validator.layer", "FlextValidatorLayer"),
    "FlextValidatorSettings": (
        "flext_tests._validator.settings",
        "FlextValidatorSettings",
    ),
    "FlextValidatorTests": ("flext_tests._validator.tests", "FlextValidatorTests"),
    "FlextValidatorTypes": ("flext_tests._validator.types", "FlextValidatorTypes"),
    "bypass": "flext_tests._validator.bypass",
    "imports": "flext_tests._validator.imports",
    "layer": "flext_tests._validator.layer",
    "models": "flext_tests._validator.models",
    "settings": "flext_tests._validator.settings",
    "tests": "flext_tests._validator.tests",
    "types": "flext_tests._validator.types",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
