# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Tests. Validator package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import _types_parts
    from .bypass import FlextTestsValidatorBypass
    from .imports import FlextTestsValidatorImports
    from .layer import FlextTestsValidatorLayer
    from .markdown import FlextTestsValidatorMarkdown
    from .settings import FlextTestsValidatorSettings
    from .tests import FlextTestsValidatorTests
    from .types import FlextTestsValidatorTypes
__all__: tuple[str, ...] = (
    "FlextTestsValidatorBypass",
    "FlextTestsValidatorImports",
    "FlextTestsValidatorLayer",
    "FlextTestsValidatorMarkdown",
    "FlextTestsValidatorSettings",
    "FlextTestsValidatorTests",
    "FlextTestsValidatorTypes",
    "_types_parts",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._types_parts": ("_types_parts",),
            ".bypass": ("FlextTestsValidatorBypass",),
            ".imports": ("FlextTestsValidatorImports",),
            ".layer": ("FlextTestsValidatorLayer",),
            ".markdown": ("FlextTestsValidatorMarkdown",),
            ".settings": ("FlextTestsValidatorSettings",),
            ".tests": ("FlextTestsValidatorTests",),
            ".types": ("FlextTestsValidatorTypes",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
