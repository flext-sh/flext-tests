"""Behavioral contract for the in-process CLI runner in ``u.Tests``.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import signal
import sys
from collections.abc import Sequence

from tests import tm, u

PROBE_ENV = "FLEXT_TESTS_IN_PROCESS_PROBE"


class TestsFlextTestsInProcess:
    """Exercise only the public result, scope and restoration guarantees."""

    @staticmethod
    def test_captures_streams_and_normalizes_system_exit() -> None:
        """A stopped entry point returns its code with both streams captured."""
        output = u.Tests.cli_in_process(TestsFlextTestsInProcess._stops, ["--flag"])

        tm.that(output.exit_code, eq=3)
        tm.that(output.stdout, eq="out\n")
        tm.that(output.stderr, eq="err\n")

    @staticmethod
    def test_empty_system_exit_is_success() -> None:
        """A bare ``SystemExit`` keeps the native zero exit code."""
        output = u.Tests.cli_in_process(TestsFlextTestsInProcess._stops_cleanly, [])

        tm.that(output.exit_code, eq=0)

    @staticmethod
    def test_environment_scope_is_owned_and_restored() -> None:
        """The declared environment is visible only during the call."""
        os.environ.pop(PROBE_ENV, None)

        output = u.Tests.cli_in_process(
            TestsFlextTestsInProcess._reads_environment,
            [],
            env={PROBE_ENV: "inside"},
        )

        tm.that(output.stdout, eq="inside\n")
        tm.ok(PROBE_ENV not in os.environ)

    @staticmethod
    def test_termination_handlers_are_restored() -> None:
        """Handlers the entry point installs do not outlive the call."""
        previous = signal.getsignal(signal.SIGTERM)
        try:
            u.Tests.cli_in_process(TestsFlextTestsInProcess._installs_handler, [])

            tm.that(signal.getsignal(signal.SIGTERM), eq=previous)
        finally:
            signal.signal(signal.SIGTERM, previous)

    @staticmethod
    def test_entrypoint_failure_propagates_and_restores_environment() -> None:
        """An unexpected failure escapes unchanged and leaves no owned variable."""
        os.environ.pop(PROBE_ENV, None)

        with u.Tests.raises(RuntimeError, match="boom"):
            u.Tests.cli_in_process(
                TestsFlextTestsInProcess._fails,
                [],
                env={PROBE_ENV: "inside"},
            )

        tm.ok(PROBE_ENV not in os.environ)

    @staticmethod
    def _stops(argv: Sequence[str]) -> int:
        del argv
        sys.stdout.write("out\n")
        sys.stderr.write("err\n")
        raise SystemExit(3)

    @staticmethod
    def _stops_cleanly(argv: Sequence[str]) -> int:
        del argv
        raise SystemExit

    @staticmethod
    def _reads_environment(argv: Sequence[str]) -> int:
        del argv
        sys.stdout.write(f"{os.environ[PROBE_ENV]}\n")
        return 0

    @staticmethod
    def _installs_handler(argv: Sequence[str]) -> int:
        del argv
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        return 0

    @staticmethod
    def _fails(argv: Sequence[str]) -> int:
        del argv
        msg = "boom"
        raise RuntimeError(msg)
