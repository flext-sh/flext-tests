"""pytest public objects the test tier reads through ``c.Tests``.

flext-tests is the pytest plugin, so pytest is a layer-zero library of its
facade families (ADR-028, operator ruling 2026-10-24); a test module never
imports pytest and reads these members instead. Each member is the pytest
object itself. The owner family follows the facade-member kind of the object
(tooling ``facade-members.owners``): constants, enums and exceptions live here.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

import pytest


class FlextTestsConstantsPytest:
    """pytest constants, enums and exceptions published under ``c.Tests``."""

    MARK: ClassVar[pytest.MarkGenerator] = pytest.mark
    FAIL: ClassVar = pytest.fail
    SKIP: ClassVar = pytest.skip
    ExitCode = pytest.ExitCode
    UsageError = pytest.UsageError


__all__: list[str] = ["FlextTestsConstantsPytest"]
