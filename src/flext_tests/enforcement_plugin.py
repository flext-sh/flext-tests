"""Lightweight class-object ``pytest11`` enforcement adapter.

Entry-point discovery precedes coverage measurement. Only lifecycle hooks
resolve the dispatcher; loading this plugin imports no fixture module.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

from flext_tests._constants.validator import FlextTestsConstantsValidator

if TYPE_CHECKING:
    import warnings

    import pytest


_DISPATCHER_MODULE = "flext_tests._fixtures._enforcement.dispatcher"


class FlextTestsEnforcementPlugin:
    """Native pytest hooks registered before option parsing by pytest11."""

    @staticmethod
    def pytest_addoption(parser: pytest.Parser) -> None:
        """Register the enforcement dispatcher's stable command-line contract."""
        parser.addini(
            FlextTestsConstantsValidator.ENFORCEMENT_SLOW_TIMEOUT_INI_OPTION,
            "Config-owned timeout in seconds for items explicitly marked slow.",
            default="",
        )
        group = parser.getgroup(
            "flext-enforce", "FLEXT cross-layer enforcement catalog"
        )
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

    @staticmethod
    def pytest_configure(config: pytest.Config) -> None:
        """Resolve enforcement only after startup instrumentation is active."""
        dispatcher = import_module(
            _DISPATCHER_MODULE,
        ).FlextTestsEnforcementDispatcher
        dispatcher.configure(config)

    @staticmethod
    def pytest_collection_modifyitems(
        session: pytest.Session,
        config: pytest.Config,
        items: list[pytest.Item],
    ) -> None:
        """Delegate collection-time enforcement."""
        dispatcher = import_module(
            _DISPATCHER_MODULE,
        ).FlextTestsEnforcementDispatcher
        dispatcher.apply_slow_budget(config, items)
        dispatcher.collection_modifyitems(session, config, items)

    @staticmethod
    def pytest_warning_recorded(
        warning_message: warnings.WarningMessage,
        when: str,
        nodeid: str,
        location: tuple[str, int, str] | None,
    ) -> None:
        """Track runtime enforcement warnings."""
        _ = when, nodeid, location
        dispatcher = import_module(
            _DISPATCHER_MODULE,
        ).FlextTestsEnforcementDispatcher
        dispatcher.record_warning(warning_message)

    @staticmethod
    def pytest_sessionstart(session: pytest.Session) -> None:
        """Expose the session config for warning-capture plumbing."""
        dispatcher = import_module(
            _DISPATCHER_MODULE,
        ).FlextTestsEnforcementDispatcher
        dispatcher.session_config = session.config

    @staticmethod
    def pytest_terminal_summary(
        terminalreporter: pytest.TerminalReporter,
        exitstatus: int,
        config: pytest.Config,
    ) -> None:
        """Delegate the enforcement summary."""
        _ = exitstatus
        dispatcher = import_module(
            _DISPATCHER_MODULE,
        ).FlextTestsEnforcementDispatcher
        dispatcher.terminal_summary(terminalreporter, config)


__all__: list[str] = []
