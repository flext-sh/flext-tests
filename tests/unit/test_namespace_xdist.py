"""xdist-parallel namespace acceptance (T3): two workers, no token overlap.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

pytest_plugins = ["pytester"]


@pytest.mark.slow
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
        "def record_token(worker_id, request):\n"
        "    run_uid = 'master'\n"
        "    if hasattr(request.config, 'workerinput'):\n"
        "        run_uid = request.config.workerinput.get('testrunuid', 'master')\n"
        "    token = u.Tests.namespace(\n"
        "        worker_id=worker_id,\n"
        "        testrun_uid=run_uid,\n"
        "        checkout_root=Path(request.config.rootpath),\n"
        "    ).token\n"
        "    (Path(request.config.rootpath) / f'{worker_id}.txt').write_text(token)\n"
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
    result = pytester.runpytest_subprocess(
        "-n",
        "2",
        "-p",
        "no:cacheprovider",
        "-p",
        "no:flext_tests_enforcement",
        "-p",
        "no:flext_infra._pytest_collection",
    )
    try:
        result.assert_outcomes(passed=2)
    except ValueError:
        import pytest

        pytest.fail(
            "inner run did not produce a summary:\n"
            + result.stdout.str()[-3000:]
            + "\nSTDERR:\n"
            + result.stderr.str()[-1500:],
        )
    tokens = {path.read_text().strip() for path in pytester.path.glob("*.txt")}
    assert len(tokens) == 2
