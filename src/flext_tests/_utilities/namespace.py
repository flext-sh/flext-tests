"""Namespace-token utilities for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import hashlib
import secrets
import time
from typing import TYPE_CHECKING

from flext_tests import m
from flext_tests._constants.namespace import FlextTestsConstantsNamespace

if TYPE_CHECKING:
    from pathlib import Path


class FlextTestsNamespaceUtilitiesMixin:
    """Pure namespace-token derivation (no I/O beyond the checkout read)."""

    @staticmethod
    def namespace(
        *, worker_id: str, testrun_uid: str, checkout_root: Path
    ) -> m.Tests.TestNamespace:
        """Derive one collision-free namespace for worker and run.

        The token is ``base36(epoch_seconds) + checkout_digest + worker_code +
        random_hex`` totalling 23 lowercase characters. Every input feeds a
        cryptographic digest or ``secrets`` randomness, so pytest-randomly
        reseeding the global random module cannot collide two runs.
        """
        epoch_stamp = _base36(int(time.time() * 1000))
        checkout_digest = hashlib.sha256(
            str(checkout_root).encode(encoding="utf-8")
        ).hexdigest()
        worker_code = _worker_code(worker_id)
        run_digest = hashlib.sha256(testrun_uid.encode(encoding="utf-8")).hexdigest()[
            :6
        ]
        random_hex = secrets.token_hex(3)
        run_token = f"{epoch_stamp}{checkout_digest[:8]}{run_digest}"
        token = f"{epoch_stamp}{checkout_digest[:8]}{worker_code}{random_hex}"
        return m.Tests.TestNamespace(
            token=token[: FlextTestsConstantsNamespace.NAMESPACE_TOKEN_LENGTH],
            run_token=run_token,
            worker=worker_id,
            checkout=checkout_digest[:8],
            issued_at_ns=time.time_ns(),
            root=str(checkout_root),
        )


def _base36(value: int) -> str:
    """Encode a non-negative integer as lowercase base36."""
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    if value == 0:
        return alphabet[0]
    encoded: list[str] = []
    while value:
        value, remainder = divmod(value, 36)
        encoded.append(alphabet[remainder])
    return "".join(reversed(encoded))


def _worker_code(worker_id: str) -> str:
    """Condense a worker identifier to two lowercase alphanumerics."""
    digest = hashlib.sha256(worker_id.encode(encoding="utf-8")).hexdigest()
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
    first = int(digest[:8], 16) % 36
    second = int(digest[8:16], 16) % 36
    return f"{alphabet[first]}{alphabet[second]}"


__all__: list[str] = ["FlextTestsNamespaceUtilitiesMixin"]
