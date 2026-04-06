# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Typings package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tests._typings.base as _flext_tests__typings_base

    base = _flext_tests__typings_base
    import flext_tests._typings.files as _flext_tests__typings_files
    from flext_tests._typings.base import FlextTestsBaseTypesMixin

    files = _flext_tests__typings_files
    import flext_tests._typings.guards as _flext_tests__typings_guards
    from flext_tests._typings.files import FlextTestsFilesTypesMixin

    guards = _flext_tests__typings_guards
    import flext_tests._typings.matchers as _flext_tests__typings_matchers
    from flext_tests._typings.guards import FlextTestsGuardsTypesMixin

    matchers = _flext_tests__typings_matchers
    from flext_tests._typings.matchers import FlextTestsMatchersTypesMixin
_LAZY_IMPORTS = {
    "FlextTestsBaseTypesMixin": (
        "flext_tests._typings.base",
        "FlextTestsBaseTypesMixin",
    ),
    "FlextTestsFilesTypesMixin": (
        "flext_tests._typings.files",
        "FlextTestsFilesTypesMixin",
    ),
    "FlextTestsGuardsTypesMixin": (
        "flext_tests._typings.guards",
        "FlextTestsGuardsTypesMixin",
    ),
    "FlextTestsMatchersTypesMixin": (
        "flext_tests._typings.matchers",
        "FlextTestsMatchersTypesMixin",
    ),
    "base": "flext_tests._typings.base",
    "files": "flext_tests._typings.files",
    "guards": "flext_tests._typings.guards",
    "matchers": "flext_tests._typings.matchers",
}

__all__ = [
    "FlextTestsBaseTypesMixin",
    "FlextTestsFilesTypesMixin",
    "FlextTestsGuardsTypesMixin",
    "FlextTestsMatchersTypesMixin",
    "base",
    "files",
    "guards",
    "matchers",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
