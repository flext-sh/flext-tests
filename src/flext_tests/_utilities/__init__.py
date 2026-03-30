# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests._utilities import matchers
    from flext_tests._utilities.matchers import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextTestsMatchersUtilities": "flext_tests._utilities.matchers",
    "matchers": "flext_tests._utilities.matchers",
    "tm": "flext_tests._utilities.matchers",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
