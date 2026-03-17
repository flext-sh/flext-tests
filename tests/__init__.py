# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package - re-exports flext_tests aliases for test convenience."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from .conftest import c, m, p, t, tb, td, tf, tk, tm, tt, u
    from .test_utils import AssertionHelpers, T, assertion_helpers

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "AssertionHelpers": ("tests.test_utils", "AssertionHelpers"),
    "T": ("tests.test_utils", "T"),
    "assertion_helpers": ("tests.test_utils", "assertion_helpers"),
    "c": ("tests.conftest", "c"),
    "m": ("tests.conftest", "m"),
    "p": ("tests.conftest", "p"),
    "t": ("tests.conftest", "t"),
    "tb": ("tests.conftest", "tb"),
    "td": ("tests.conftest", "td"),
    "tf": ("tests.conftest", "tf"),
    "tk": ("tests.conftest", "tk"),
    "tm": ("tests.conftest", "tm"),
    "tt": ("tests.conftest", "tt"),
    "u": ("tests.conftest", "u"),
}

__all__ = [
    "AssertionHelpers",
    "T",
    "assertion_helpers",
    "c",
    "m",
    "p",
    "t",
    "tb",
    "td",
    "tf",
    "tk",
    "tm",
    "tt",
    "u",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
