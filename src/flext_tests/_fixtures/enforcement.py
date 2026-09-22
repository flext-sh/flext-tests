"""Pytest dispatcher facade for the cross-layer enforcement catalog."""

from __future__ import annotations

from flext_tests.enforcement_plugin import pytest_addoption, pytest_warning_recorded

from ._enforcement_parts.config import (
    active_rules,
    discover_repository_root,
    pytest_configure,
    split_csv,
)
from ._enforcement_parts.hooks import (
    pytest_collection_modifyitems,
    pytest_sessionstart,
    pytest_terminal_summary,
)
from ._enforcement_parts import (
    _EnforcementCollector,
    FlextTestsEnforcementItem,
    _EnforcementViolationError,
)

__all__: list[str] = [
    "_EnforcementCollector",
    "FlextTestsEnforcementItem",
    "_EnforcementViolationError",
    "active_rules",
    "discover_repository_root",
    "pytest_addoption",
    "pytest_collection_modifyitems",
    "pytest_configure",
    "pytest_sessionstart",
    "pytest_terminal_summary",
    "pytest_warning_recorded",
    "split_csv",
]
