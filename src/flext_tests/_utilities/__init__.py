# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_tests._utilities._payload import *
    from flext_tests._utilities.matchers import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
