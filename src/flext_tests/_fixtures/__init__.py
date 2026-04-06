# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Fixtures package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_tests._fixtures.settings import (
        T,
        reset_settings,
        settings,
        settings_factory,
    )
_LAZY_IMPORTS = {
    "T": ("flext_tests._fixtures.settings", "T"),
    "reset_settings": ("flext_tests._fixtures.settings", "reset_settings"),
    "settings": ("flext_tests._fixtures.settings", "settings"),
    "settings_factory": ("flext_tests._fixtures.settings", "settings_factory"),
}

__all__ = [
    "T",
    "reset_settings",
    "settings",
    "settings_factory",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
