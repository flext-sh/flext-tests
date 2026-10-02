"""Per-checkout scratch storage resolution for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from flext_tests import c


class FlextTestsScratchStorageUtilitiesMixin:
    """Scratch-root derivation; pure path logic over the constants facade."""

    @staticmethod
    def scratch_root(*, checkout_root: Path, override: str | None = None) -> Path:
        """Return the per-checkout scratch directory (created on demand).

        Storage law: caches never live inside the checkout. The directory is
        keyed by the checkout's absolute path so two checkouts never share a
        database; an explicit ``override`` (declared via the
        ``flext_scratch_root`` ini) replaces the host default.
        """
        identity = hashlib.sha256(
            str(checkout_root).encode(encoding="utf-8")
        ).hexdigest()[:12]
        base = (
            Path(override)
            if override
            else Path.home().joinpath(*c.Tests.SCRATCH_DIR_PARTS)
        )
        scratch = base / identity
        scratch.mkdir(parents=True, exist_ok=True)
        return scratch


__all__: list[str] = ["FlextTestsScratchStorageUtilitiesMixin"]
