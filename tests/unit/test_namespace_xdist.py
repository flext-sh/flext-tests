"""xdist-parallel namespace acceptance (T3): two workers, no token overlap.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import os
import signal
from pathlib import Path
from types import FrameType
from typing import Final, NoReturn

import pytest

from tests import tm, u

pytest_plugins = ["pytester"]

XDIST_WORKER_COUNT: Final[int] = 2


class TestsFlextTestsNamespaceXdist:
    """xdist-parallel namespace acceptance (T3)."""

    @staticmethod
    @pytest.mark.slow
    def test_pytest_subprocess_reaps_on_base_exception(
        pytester: pytest.Pytester,
    ) -> None:
        """An external cancellation reaps its exact child before propagating."""

        class Cancelled(BaseException):
            """External item cancellation, not a child execution failure."""

        cancellation = Cancelled("cancel isolated consumer")

        def cancel(_number: int, _frame: FrameType | None) -> NoReturn:
            raise cancellation

        pytester.makepyfile(
            test_cancel=(
                "import os\n"
                "import signal\n"
                "from pathlib import Path\n"
                "def test_cancel():\n"
                "    Path('child.pid').write_text(str(os.getpid()))\n"
                f"    os.kill({os.getpid()}, signal.SIGUSR1)\n"
                "    signal.pause()\n"
            ),
        )
        previous = signal.signal(signal.SIGUSR1, cancel)
        try:
            with pytest.raises(Cancelled) as raised:
                u.Tests.pytest_subprocess(pytester)
        finally:
            signal.signal(signal.SIGUSR1, previous)
        tm.ok(raised.value is cancellation)
        child_pid = int((pytester.path / "child.pid").read_text(encoding="utf-8"))
        with pytest.raises(ProcessLookupError):
            os.kill(child_pid, 0)
        with pytest.raises(ChildProcessError):
            os.waitpid(child_pid, os.WNOHANG)

    @pytest.mark.slow
    @staticmethod
    def test_namespaces_unique_across_two_workers(pytester: pytest.Pytester) -> None:
        """Pytest -n 2 derives distinct tokens per worker (recorded to files)."""
        pytester.makeconftest(
            # NOTE: flext_tests.conftest_plugin auto-loads via the pytest11 entry
            # point; declaring it in pytest_plugins double-registers and aborts.
            "import pytest\n"
            "from pathlib import Path\n"
            "from flext_tests import u\n"
            "\n"
            "@pytest.fixture(scope='session')\n"
            "def record_token(worker_id, request, session_runtime):\n"
            "    run_uid = 'master'\n"
            "    if hasattr(request.config, 'workerinput'):\n"
            "        run_uid = request.config.workerinput.get("
            "'testrunuid', 'master')\n"
            "    token = u.Tests.namespace(\n"
            "        worker_id=worker_id,\n"
            "        testrun_uid=run_uid,\n"
            "        checkout_root=Path(request.config.rootpath),\n"
            "    ).token\n"
            "    (Path(request.config.rootpath) / "
            "f'{worker_id}.txt').write_text("
            "f'{token}\\n{session_runtime.directory}')\n"
            "    assert not (session_runtime.directory / 'project').exists()\n"
            "    return token\n",
        )
        pytester.makepyfile(
            test_a="""
            def test_a(record_token):
                assert record_token
            """,
            test_b="""
            def test_b(record_token):
                assert record_token
            """,
        )
        result = u.Tests.pytest_subprocess(
            pytester,
            "-n",
            "2",
            "-p",
            "no:cacheprovider",
            "-p",
            "no:flext_tests_enforcement",
            "-p",
            "no:flext_infra._pytest.collection",
        )
        try:
            result.assert_outcomes(passed=2)
        except ValueError:
            pytest.fail(
                "inner run did not produce a summary:\n"
                + result.stdout.str()[-3000:]
                + "\nSTDERR:\n"
                + result.stderr.str()[-1500:],
            )
        records = [
            path.read_text().splitlines() for path in pytester.path.glob("*.txt")
        ]
        tokens = {record[0] for record in records}
        tm.that(len(tokens), eq=XDIST_WORKER_COUNT)
        directories = {Path(record[1]) for record in records}
        tm.that(len(directories), eq=XDIST_WORKER_COUNT)
        tm.that(all(not directory.exists() for directory in directories), truth=True)
