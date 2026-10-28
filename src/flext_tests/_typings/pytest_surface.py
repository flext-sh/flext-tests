"""pytest public types the test tier reads through ``t.Tests``.

flext-tests is the pytest plugin, so pytest is a layer-zero library of its
facade families (ADR-028, operator ruling 2026-10-24); a test module never
imports pytest and reads these members instead. The types are declared once,
by flext-infra's ``t.Infra.Pytest``; this mixin publishes them under
``t.Tests`` by inheritance.

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

from flext_infra import FlextInfraTypes


class FlextTestsTypesPytest(FlextInfraTypes.Infra.Pytest):
    """pytest types published under ``t.Tests``, owned by ``t.Infra.Pytest``."""


__all__: list[str] = ["FlextTestsTypesPytest"]
