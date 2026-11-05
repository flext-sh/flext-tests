"""Scenario data: connectivity and remote-gated tests next to a pure integration test.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest


@pytest.mark.parametrize("marker", ["connectivity"])
def test_external(marker: str) -> None:
    """Fail loudly if collection runs a test whose capability is absent."""
    pytest.fail(f"test executed under the {marker} capability")


@pytest.mark.remote
def test_remote_gate() -> None:
    """Runs: a generic external gate is never a local .env prerequisite."""


@pytest.mark.integration
def test_pure_integration() -> None:
    """Runs: integration alone needs no external capability."""
