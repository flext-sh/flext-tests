"""pytest public objects the test tier reads through ``c.Tests``.

flext-tests is the pytest plugin, so pytest is a layer-zero library of its
facade families (ADR-028, operator ruling 2026-10-24); a test module never
imports pytest and reads these members instead. Constants, enums and
exceptions are declared once, by flext-infra's ``c.Infra.Pytest``; this
class publishes them under ``c.Tests`` by inheritance.

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

from flext_infra import FlextInfraConstants


class FlextTestsConstantsPytest(FlextInfraConstants.Infra.Pytest):
    """pytest constants published under ``c.Tests``, owned by ``c.Infra.Pytest``."""


__all__: list[str] = ["FlextTestsConstantsPytest"]
