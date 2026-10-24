"""Contract of the scenario fixture-tree materializer.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable


class FlextTestsFixtureTreesProtocolsMixin:
    """Callable the ``fixture_tree`` fixture hands to a test."""

    @runtime_checkable
    class FixtureTree(Protocol):
        """Copy one scenario tree; ``destination`` defaults to ``tmp_path``."""

        def __call__(self, scenario: str, destination: Path = ...) -> Path:
            """Materialize ``scenario`` and return its destination."""
            ...


__all__: list[str] = ["FlextTestsFixtureTreesProtocolsMixin"]
