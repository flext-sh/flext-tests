# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Protocols package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tests._protocols.valuefactory as _flext_tests__protocols_valuefactory

    valuefactory = _flext_tests__protocols_valuefactory
    from flext_tests._protocols.valuefactory import FlextTestsValueFactoryProtocolsMixin
_LAZY_IMPORTS = {
    "FlextTestsValueFactoryProtocolsMixin": (
        "flext_tests._protocols.valuefactory",
        "FlextTestsValueFactoryProtocolsMixin",
    ),
    "valuefactory": "flext_tests._protocols.valuefactory",
}

__all__ = [
    "FlextTestsValueFactoryProtocolsMixin",
    "valuefactory",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
