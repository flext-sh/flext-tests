"""pytest public types the test tier reads through ``t.Tests``.

flext-tests is the pytest plugin, so pytest is a layer-zero library of its
facade families (ADR-028, operator ruling 2026-10-24); a test module never
imports pytest and reads these members instead. Each member is the pytest
class itself, valid both in annotations and at runtime.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest


class FlextTestsPytestTypesMixin:
    """pytest classes published under ``t.Tests``."""

    CaptureFixture = pytest.CaptureFixture
    Config = pytest.Config
    FixtureRequest = pytest.FixtureRequest
    LogCaptureFixture = pytest.LogCaptureFixture
    Metafunc = pytest.Metafunc
    MonkeyPatch = pytest.MonkeyPatch
    Pytester = pytest.Pytester
    RunResult = pytest.RunResult
    StashKey = pytest.StashKey
    TempPathFactory = pytest.TempPathFactory


__all__: list[str] = ["FlextTestsPytestTypesMixin"]
