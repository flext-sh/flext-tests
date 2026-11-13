"""Shared scratch storage resolution for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_tests import c


class FlextTestsUtilitiesScratchStorage:
    """Scratch-root derivation; pure path logic over the constants facade."""

    @staticmethod
    def scratch_root(*, override: str | None = None) -> Path:
        """Return the scratch directory every checkout and run shares.

        Its entries are keyed by their own content (for example a dependency
        wheel by the digest of its sources), so a checkout path never
        multiplies them; an explicit ``override`` (declared via the
        ``flext_scratch_root`` ini) replaces the host default.
        """
        scratch = (
            Path(override)
            if override
            else Path.home().joinpath(*c.Tests.SCRATCH_DIR_PARTS)
        )
        scratch.mkdir(parents=True, exist_ok=True)
        return scratch


__all__: list[str] = ["FlextTestsUtilitiesScratchStorage"]
