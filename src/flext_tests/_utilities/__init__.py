# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tests._utilities._payload as _flext_tests__utilities__payload

    _payload = _flext_tests__utilities__payload
    import flext_tests._utilities.matchers as _flext_tests__utilities_matchers
    from flext_tests._utilities._payload import (
        FlextTestsPayloadUtilities,
        deep_match,
        length_validate,
        to_config_map_value,
        to_normalized_value,
        to_payload,
    )

    matchers = _flext_tests__utilities_matchers
    from flext_tests._utilities.matchers import FlextTestsMatchersUtilities, tm
_LAZY_IMPORTS = {
    "FlextTestsMatchersUtilities": "flext_tests._utilities.matchers",
    "FlextTestsPayloadUtilities": "flext_tests._utilities._payload",
    "_payload": "flext_tests._utilities._payload",
    "deep_match": "flext_tests._utilities._payload",
    "length_validate": "flext_tests._utilities._payload",
    "matchers": "flext_tests._utilities.matchers",
    "tm": "flext_tests._utilities.matchers",
    "to_config_map_value": "flext_tests._utilities._payload",
    "to_normalized_value": "flext_tests._utilities._payload",
    "to_payload": "flext_tests._utilities._payload",
}

__all__ = [
    "FlextTestsMatchersUtilities",
    "FlextTestsPayloadUtilities",
    "_payload",
    "deep_match",
    "length_validate",
    "matchers",
    "tm",
    "to_config_map_value",
    "to_normalized_value",
    "to_payload",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
