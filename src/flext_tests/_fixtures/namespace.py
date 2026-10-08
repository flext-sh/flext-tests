"""Canonical namespace fixtures shared by every consumer suite.

The ``u`` facade loads the model tree, so it resolves through the deferred
``import_module`` form inside the fixture bodies: registering this module at
configure time never loads ``flext_tests.models``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from flext_tests import m


def _worker_id(config: pytest.Config) -> str:
    """Resolve the xdist worker id (master outside xdist).

    Returns:
        The resulting ``str``.
    """
    worker_input = getattr(config, "workerinput", None)
    if worker_input is not None:
        return str(worker_input.get("workerid", "master"))
    return "master"


def _run_token(config: pytest.Config) -> str:
    """Resolve the shared run token (xdist testrunuid or session-stable id).

    Returns:
        The resulting ``str``.
    """
    worker_input = getattr(config, "workerinput", None)
    if worker_input is not None:
        return str(worker_input.get("testrunuid", ""))
    stash_key = pytest.StashKey[str]()
    if stash_key not in config.stash:
        config.stash[stash_key] = (
            import_module("flext_tests")
            .u.Tests.namespace(
                worker_id="master",
                testrun_uid=f"master-{id(config)}",
                checkout_root=Path(config.rootpath),
            )
            .token
        )
    return config.stash[stash_key]


@pytest.fixture(scope="session")
def run_namespace(request: pytest.FixtureRequest) -> m.Tests.TestNamespace:
    """Session namespace: one token per pytest run per worker.

    Returns:
        The resulting ``m.Tests.TestNamespace``.
    """
    config = request.config
    namespace: m.Tests.TestNamespace = import_module("flext_tests").u.Tests.namespace(
        worker_id=_worker_id(config),
        testrun_uid=_run_token(config),
        checkout_root=Path(config.rootpath),
    )
    return namespace


@pytest.fixture
def test_namespace(run_namespace: m.Tests.TestNamespace) -> m.Tests.TestNamespace:
    """Function namespace: the run token plus a fresh per-test token.

    Returns:
        The resulting ``m.Tests.TestNamespace``.
    """
    namespace: m.Tests.TestNamespace = import_module("flext_tests").u.Tests.namespace(
        worker_id=run_namespace.worker,
        testrun_uid=f"{run_namespace.run_token}-{run_namespace.issued_at_ns}",
        checkout_root=Path(run_namespace.root),
    )
    return namespace
