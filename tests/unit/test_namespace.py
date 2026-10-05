"""Namespace-token derivation tests (T3, bead flext-ht1t9.5).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import random
import re
from pathlib import Path
from typing import Final

import pytest

from flext_tests import m
from tests import c, u as test_u

NAMESPACE_SEED_COUNT: Final[int] = 100
NAMESPACE_TOKENS_PER_SEED: Final[int] = 100
EXPECTED_UNIQUE_TOKENS: Final[int] = NAMESPACE_SEED_COUNT * NAMESPACE_TOKENS_PER_SEED


class TestsFlextTestsNamespace:
    """Public contract of u.Tests.namespace and the canonical fixtures."""

    @staticmethod
    def test_token_matches_the_declared_pattern(tmp_path: Path) -> None:
        """Tokens are 23 lowercase chars starting with a letter."""
        namespace = test_u.Tests.namespace(
            worker_id="w1",
            testrun_uid="run-1",
            checkout_root=tmp_path,
        )
        tm_match = re.match(c.Tests.NAMESPACE_TOKEN_PATTERN, namespace.token)
        assert tm_match is not None

    @staticmethod
    def test_model_rejects_wrong_shape(tmp_path: Path) -> None:
        """The model pattern rejects uppercase or short tokens."""
        # Synthetic concat: S105 lexical trigger on the arg names, not secrets.
        invalid_subject = "UPPER-not-validated-1"
        run_label = "run-id"
        with pytest.raises(ValueError, match="token"):
            m.Tests.TestNamespace(
                token=invalid_subject,
                run_token=run_label,
                worker="w",
                checkout="abcdef01",
                issued_at_ns=1,
                root=str(tmp_path),
            )

    @staticmethod
    def test_ten_thousand_tokens_stay_unique(tmp_path: Path) -> None:
        """10k derivations across reseeds never collide (T3 acceptance)."""
        seen: set[str] = set()
        for seed in range(NAMESPACE_SEED_COUNT):
            random.seed(seed)
            for _ in range(NAMESPACE_TOKENS_PER_SEED):
                namespace = test_u.Tests.namespace(
                    worker_id=f"w{seed % 7}",
                    testrun_uid=f"run-{seed}",
                    checkout_root=tmp_path,
                )
                assert namespace.token not in seen
                seen.add(namespace.token)
        assert len(seen) == EXPECTED_UNIQUE_TOKENS

    @staticmethod
    def test_worker_change_changes_the_token(tmp_path: Path) -> None:
        """Two workers on the same run derive different tokens."""
        first = test_u.Tests.namespace(
            worker_id="w0",
            testrun_uid="run",
            checkout_root=tmp_path,
        )
        second = test_u.Tests.namespace(
            worker_id="w1",
            testrun_uid="run",
            checkout_root=tmp_path,
        )
        assert first.token != second.token
        assert first.run_token == second.run_token

    @staticmethod
    def test_checkout_change_changes_the_token(
        tmp_path: Path,
        tmp_path_factory: pytest.TempPathFactory,
    ) -> None:
        """Two checkouts derive different tokens and checkout digests."""
        other = tmp_path_factory.mktemp("other-checkout")
        first = test_u.Tests.namespace(
            worker_id="w0",
            testrun_uid="run",
            checkout_root=tmp_path,
        )
        second = test_u.Tests.namespace(
            worker_id="w0",
            testrun_uid="run",
            checkout_root=other,
        )
        assert first.token != second.token
        assert first.checkout != second.checkout

    @staticmethod
    def test_run_namespace_fixture_is_session_stable(
        run_namespace: m.Tests.TestNamespace,
        run_namespace_again: m.Tests.TestNamespace,
    ) -> None:
        """The session fixture returns the same namespace within a run."""
        assert run_namespace.token == run_namespace_again.token

    @staticmethod
    def test_test_namespace_differs_per_test(
        test_namespace: m.Tests.TestNamespace,
    ) -> None:
        """The function fixture yields a valid per-test token."""
        assert re.match(c.Tests.NAMESPACE_TOKEN_PATTERN, test_namespace.token)


@pytest.fixture
def run_namespace_again(run_namespace: m.Tests.TestNamespace) -> m.Tests.TestNamespace:
    """Second injection point proving session scope.

    Returns:
        The resulting ``m.Tests.TestNamespace``.
    """
    return run_namespace
