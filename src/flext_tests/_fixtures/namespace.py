"""Canonical namespace fixtures shared by every consumer suite.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from flext_tests import m


def _worker_id(config: pytest.Config) -> str:
    """Resolve the xdist worker id (master outside xdist)."""
    worker_input = getattr(config, "workerinput", None)
    if worker_input is not None:
        return str(worker_input.get("workerid", "master"))
    return "master"


def _run_token(config: pytest.Config) -> str:
    """Resolve the shared run token (xdist testrunuid or session-stable id)."""
    from flext_tests import u

    worker_input = getattr(config, "workerinput", None)
    if worker_input is not None:
        return str(worker_input.get("testrunuid", ""))
    stash_key = pytest.StashKey[str]()
    if stash_key not in config.stash:
        config.stash[stash_key] = u.Tests.namespace(
            worker_id="master",
            testrun_uid=f"master-{id(config)}",
            checkout_root=Path(config.rootpath),
        ).token
    return config.stash[stash_key]


@pytest.fixture(scope="session")
def run_namespace(request: pytest.FixtureRequest) -> m.Tests.TestNamespace:
    """Session namespace: one token per pytest run per worker."""
    from flext_tests import u

    config = request.config
    return u.Tests.namespace(
        worker_id=_worker_id(config),
        testrun_uid=_run_token(config),
        checkout_root=Path(config.rootpath),
    )


@pytest.fixture
def test_namespace(run_namespace: m.Tests.TestNamespace) -> m.Tests.TestNamespace:
    """Function namespace: the run token plus a fresh per-test token."""
    from flext_tests import u

    return u.Tests.namespace(
        worker_id=run_namespace.worker,
        testrun_uid=f"{run_namespace.run_token}-{run_namespace.issued_at_ns}",
        checkout_root=Path(run_namespace.root),
    )
