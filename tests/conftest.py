"""Shared pytest configuration for the flext-tests test suite."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import t

pytest_plugins: t.VariadicTuple[str] = ("pytester",)
