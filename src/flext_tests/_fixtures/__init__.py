# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Fixtures package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_tests._fixtures.settings as _flext_tests__fixtures_settings

    settings = _flext_tests__fixtures_settings
    from flext_tests._fixtures.settings import T
_LAZY_IMPORTS = {
    "T": ("flext_tests._fixtures.settings", "T"),
    "settings": "flext_tests._fixtures.settings",
}

__all__ = [
    "T",
    "settings",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
