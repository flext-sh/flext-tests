"""Test-domain file helpers (size formatting only).

Format detection lives in the ``u.Cli`` canonical helpers; no I/O lives here.

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

from flext_tests import c


class FlextTestsUtilitiesFiles:
    """Test-only file helpers that have no ``u.Cli`` counterpart."""

    # NOTE (multi-agent): format_size moved here from c.Tests constants facet
    # (declaration purity - constants must not hold formatting behavior; mro-i6nq.11).
    @staticmethod
    def format_size(size: int) -> str:
        """Format a byte size in human-readable units (e.g. "1.2 KB").

        Returns:
            The resulting ``str``.

        """
        value = size
        for unit in c.Tests.SIZE_UNITS:
            if value < c.Tests.SIZE_THRESHOLD:
                return f"{value:.1f} {unit}" if unit != "B" else f"{value} {unit}"
            value //= c.Tests.SIZE_THRESHOLD
        return f"{value:.1f} PB"


__all__: list[str] = ["FlextTestsUtilitiesFiles"]
