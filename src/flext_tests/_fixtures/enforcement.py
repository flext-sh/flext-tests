"""Pytest dispatcher facade for the cross-layer enforcement catalog."""

from __future__ import annotations

from flext_tests.enforcement_plugin import pytest_addoption, pytest_warning_recorded

from ._enforcement_parts import FlextTestsEnforcementItem
from ._enforcement_parts._collector import FlextTestsEnforcementCollector
from ._enforcement_parts._error import FlextTestsEnforcementViolationError
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

__all__: list[str] = [
    "FlextTestsEnforcementCollector",
    "FlextTestsEnforcementItem",
    "FlextTestsEnforcementViolationError",
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
