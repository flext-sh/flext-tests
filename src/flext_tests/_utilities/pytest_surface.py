"""pytest public functions the test tier calls through ``u.Tests``.

flext-tests is the pytest plugin, so pytest is a layer-zero library of its
facade families (ADR-028, operator ruling 2026-10-24); a test module never
imports pytest and calls these members instead. The functions are declared
once, by flext-infra's ``u.Infra.Pytest``; this mixin publishes them under
``u.Tests`` by inheritance.

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

from flext_infra import FlextInfraUtilities


class FlextTestsUtilitiesPytest(FlextInfraUtilities.Infra.Pytest):
    """pytest functions published under ``u.Tests``, owned by ``u.Infra.Pytest``."""


__all__: list[str] = ["FlextTestsUtilitiesPytest"]
