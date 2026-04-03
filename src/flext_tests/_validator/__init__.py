# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Validator package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests._validator import (
        bypass,
        imports,
        layer,
        models,
        settings,
        tests,
        types,
    )
    from flext_tests._validator.bypass import FlextValidatorBypass
    from flext_tests._validator.imports import FlextValidatorImports
    from flext_tests._validator.layer import FlextValidatorLayer
    from flext_tests._validator.models import FlextValidatorModels, vm
    from flext_tests._validator.settings import FlextValidatorSettings
    from flext_tests._validator.tests import FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextValidatorBypass": "flext_tests._validator.bypass",
    "FlextValidatorImports": "flext_tests._validator.imports",
    "FlextValidatorLayer": "flext_tests._validator.layer",
    "FlextValidatorModels": "flext_tests._validator.models",
    "FlextValidatorSettings": "flext_tests._validator.settings",
    "FlextValidatorTests": "flext_tests._validator.tests",
    "FlextValidatorTypes": "flext_tests._validator.types",
    "bypass": "flext_tests._validator.bypass",
    "imports": "flext_tests._validator.imports",
    "layer": "flext_tests._validator.layer",
    "models": "flext_tests._validator.models",
    "settings": "flext_tests._validator.settings",
    "tests": "flext_tests._validator.tests",
    "types": "flext_tests._validator.types",
    "vm": "flext_tests._validator.models",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
