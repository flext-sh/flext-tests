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
    """pytest types published under ``t.Tests``.

    Test modules use these only in annotations, so they are PEP 695 aliases
    (not fields). ``StashKey`` is constructed at runtime
    (``StashKey[T]()``) and ``failed`` is caught at runtime
    (``u.Tests.raises(t.Tests.failed)``), so both stay fields bound to the
    class itself; fields binding a library class are snake_case (operator
    ruling operator-ruling-2026-10-24-sonar-s116-snake-case-scope).
    """

    type CaptureFixture[AnyStrT: (str, bytes)] = pytest.CaptureFixture[AnyStrT]
    type Config = pytest.Config
    type FixtureRequest = pytest.FixtureRequest
    type LogCaptureFixture = pytest.LogCaptureFixture
    type Metafunc = pytest.Metafunc
    type MonkeyPatch = pytest.MonkeyPatch
    type Pytester = pytest.Pytester
    type RunResult = pytest.RunResult
    type TempPathFactory = pytest.TempPathFactory
    StashKey = pytest.StashKey
    failed = pytest.fail.Exception


__all__: list[str] = ["FlextTestsPytestTypesMixin"]
