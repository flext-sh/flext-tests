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
    from flext_tests._validator.bypass import *
    from flext_tests._validator.imports import *
    from flext_tests._validator.layer import *
    from flext_tests._validator.models import *
    from flext_tests._validator.settings import *
    from flext_tests._validator.tests import *
    from flext_tests._validator.types import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
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
