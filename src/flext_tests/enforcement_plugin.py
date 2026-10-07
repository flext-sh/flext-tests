"""Lightweight ``pytest11`` adapter for the enforcement dispatcher.

This module owns only the external pytest hook boundary; the enforcement
contract itself lives in ``flext_tests._fixtures._enforcement_parts.dispatcher``,
imported at module level per the fleet's no-mid-code-imports law.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_tests._fixtures._enforcement_parts.dispatcher import (
    FlextTestsEnforcementDispatcher,
)

if TYPE_CHECKING:
    import warnings

    import pytest

SLOW_TIMEOUT_INI_OPTION = "flext_slow_timeout_seconds"
"""Config-owned timeout option for slow pytest items."""


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register the enforcement dispatcher's stable command-line contract."""
    parser.addini(
        SLOW_TIMEOUT_INI_OPTION,
        "Config-owned timeout in seconds for items explicitly marked slow.",
        default="",
    )
    group = parser.getgroup("flext-enforce", "FLEXT cross-layer enforcement catalog")
    group.addoption(
        "--flext-enforce",
        action="store_true",
        default=False,
        help=(
            "Force-enable the FLEXT enforcement dispatcher (default: auto - "
            "enabled when the pytest rootdir is the workspace root)."
        ),
    )
    group.addoption(
        "--no-flext-enforce",
        action="store_true",
        default=False,
        help="Disable the FLEXT enforcement dispatcher.",
    )
    group.addoption(
        "--flext-enforce-strict",
        action="store_true",
        default=False,
        help="Promote runtime enforcement warnings to pytest failures.",
    )
    group.addoption(
        "--flext-enforce-rules",
        action="store",
        default="",
        help="Comma-separated ENFORCE-NNN allow list.",
    )
    group.addoption(
        "--flext-enforce-exclude-rules",
        action="store",
        default="",
        help="Comma-separated ENFORCE-NNN block list.",
    )
    group.addoption(
        "--flext-enforce-workspace-root",
        action="store",
        default="",
        help="Override workspace root auto-detection with an explicit path.",
    )


def pytest_configure(config: pytest.Config) -> None:
    """Resolve enforcement only after startup instrumentation is active."""
    dispatcher = FlextTestsEnforcementDispatcher
    dispatcher.configure(config)


def pytest_collection_modifyitems(
    session: pytest.Session,
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Delegate collection-time enforcement."""
    dispatcher = FlextTestsEnforcementDispatcher
    dispatcher.collection_modifyitems(session, config, items)


def pytest_warning_recorded(
    warning_message: warnings.WarningMessage,
    when: str,
    nodeid: str,
    location: tuple[str, int, str] | None,
) -> None:
    """Track runtime enforcement warnings."""
    _ = when, nodeid, location
    dispatcher = FlextTestsEnforcementDispatcher
    dispatcher.record_warning(warning_message)


def pytest_sessionstart(session: pytest.Session) -> None:
    """Expose the session config for warning-capture plumbing."""
    dispatcher = FlextTestsEnforcementDispatcher
    dispatcher.session_config = session.config


def pytest_terminal_summary(
    terminalreporter: pytest.TerminalReporter,
    exitstatus: int,
    config: pytest.Config,
) -> None:
    """Delegate the enforcement summary."""
    _ = exitstatus
    dispatcher = FlextTestsEnforcementDispatcher
    dispatcher.terminal_summary(terminalreporter, config)


__all__: list[str] = [
    "SLOW_TIMEOUT_INI_OPTION",
    "pytest_addoption",
    "pytest_collection_modifyitems",
    "pytest_configure",
    "pytest_sessionstart",
    "pytest_terminal_summary",
    "pytest_warning_recorded",
]
