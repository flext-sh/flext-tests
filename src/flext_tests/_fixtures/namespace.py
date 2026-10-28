"""Canonical namespace fixtures shared by every consumer suite.

Namespace creation remains fixture-driven; importing a shared facade does not
activate enforcement or execute consumer tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path

import pytest

from flext_tests import m


class FlextTestsNamespaceFixtures:
    """One native plugin owner for worker-session and function namespaces."""

    @staticmethod
    def _worker_id(config: pytest.Config) -> str:
        """Resolve the xdist worker id (master outside xdist).

        Returns:
            str: The xdist worker id, or "master" outside xdist.

        """
        worker_input = getattr(config, "workerinput", None)
        if worker_input is not None:
            return str(worker_input.get("workerid", "master"))
        return "master"

    @staticmethod
    def _run_token(config: pytest.Config) -> str:
        """Resolve the shared run token (xdist testrunuid or session-stable id).

        Returns:
            str: The shared run token for this pytest run.

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
    @staticmethod
    def run_namespace(request: pytest.FixtureRequest) -> m.Tests.TestNamespace:
        """Session namespace: one token per pytest run per worker.

        Returns:
            m.Tests.TestNamespace: The session-scoped test namespace.

        """
        config = request.config
        namespace: m.Tests.TestNamespace = import_module(
            "flext_tests"
        ).u.Tests.namespace(
            worker_id=FlextTestsNamespaceFixtures._worker_id(config),
            testrun_uid=FlextTestsNamespaceFixtures._run_token(config),
            checkout_root=Path(config.rootpath),
        )
        return namespace
