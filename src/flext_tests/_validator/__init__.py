# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Validator extensions for FLEXT architecture validation.

Internal module providing specialized validation methods.
Use via FlextTestsValidator (tv) in validator.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._validator import (
        bypass as bypass,
        imports as imports,
        layer as layer,
        models as models,
        settings as settings,
        tests as tests,
        types as types,
    )
    from flext_tests._validator.bypass import (
        FlextValidatorBypass as FlextValidatorBypass,
    )
    from flext_tests._validator.imports import (
        FlextValidatorImports as FlextValidatorImports,
    )
    from flext_tests._validator.layer import FlextValidatorLayer as FlextValidatorLayer
    from flext_tests._validator.models import (
        FlextValidatorModels as FlextValidatorModels,
        vm as vm,
    )
    from flext_tests._validator.settings import (
        FlextValidatorSettings as FlextValidatorSettings,
    )
    from flext_tests._validator.tests import FlextValidatorTests as FlextValidatorTests
    from flext_tests._validator.types import FlextValidatorTypes as FlextValidatorTypes

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextValidatorBypass": ["flext_tests._validator.bypass", "FlextValidatorBypass"],
    "FlextValidatorImports": [
        "flext_tests._validator.imports",
        "FlextValidatorImports",
    ],
    "FlextValidatorLayer": ["flext_tests._validator.layer", "FlextValidatorLayer"],
    "FlextValidatorModels": ["flext_tests._validator.models", "FlextValidatorModels"],
    "FlextValidatorSettings": [
        "flext_tests._validator.settings",
        "FlextValidatorSettings",
    ],
    "FlextValidatorTests": ["flext_tests._validator.tests", "FlextValidatorTests"],
    "FlextValidatorTypes": ["flext_tests._validator.types", "FlextValidatorTypes"],
    "bypass": ["flext_tests._validator.bypass", ""],
    "imports": ["flext_tests._validator.imports", ""],
    "layer": ["flext_tests._validator.layer", ""],
    "models": ["flext_tests._validator.models", ""],
    "settings": ["flext_tests._validator.settings", ""],
    "tests": ["flext_tests._validator.tests", ""],
    "types": ["flext_tests._validator.types", ""],
    "vm": ["flext_tests._validator.models", "vm"],
}

_EXPORTS: Sequence[str] = [
    "FlextValidatorBypass",
    "FlextValidatorImports",
    "FlextValidatorLayer",
    "FlextValidatorModels",
    "FlextValidatorSettings",
    "FlextValidatorTests",
    "FlextValidatorTypes",
    "bypass",
    "imports",
    "layer",
    "models",
    "settings",
    "tests",
    "types",
    "vm",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
