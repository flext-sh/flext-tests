"""Namespace-token utilities for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import hashlib
import secrets
import threading
import time
from typing import TYPE_CHECKING, ClassVar

from flext_tests import m
from flext_tests._constants.namespace import FlextTestsConstantsNamespace

if TYPE_CHECKING:
    from pathlib import Path


class FlextTestsNamespaceUtilitiesMixin:
    """Pure namespace-token derivation (no I/O beyond the checkout read)."""

    _issue_lock: ClassVar[threading.Lock] = threading.Lock()
    _last_issue: ClassVar[tuple[int, int] | None] = None

    @staticmethod
    def namespace(
        *,
        worker_id: str,
        testrun_uid: str,
        checkout_root: Path,
    ) -> m.Tests.TestNamespace:
        """Derive one collision-free namespace for worker and run.

        The token is ``base36(epoch_milliseconds) + checkout_digest +
        worker_code + tail``, exactly ``NAMESPACE_TOKEN_LENGTH`` lowercase
        characters. The tail is monotonic within one millisecond of one
        process (the previous tail plus one), so a process never issues the
        same token twice; a new millisecond starts the tail from ``secrets``
        randomness, which separates concurrent processes and is immune to
        pytest-randomly reseeding the global random module. The run token
        derives only from the checkout and ``testrun_uid``, so every worker
        and every call of one run shares it whatever the clock reads.

        Returns:
            The resulting ``m.Tests.TestNamespace``.
        """
        namespace_constants = FlextTestsConstantsNamespace
        issued_ms = time.time_ns() // 1_000_000
        epoch_stamp = FlextTestsNamespaceUtilitiesMixin._base36(issued_ms)
        checkout_digest = hashlib.sha256(
            str(checkout_root).encode(encoding="utf-8"),
        ).hexdigest()[: namespace_constants.NAMESPACE_CHECKOUT_DIGEST_LENGTH]
        worker_code = FlextTestsNamespaceUtilitiesMixin._worker_code(worker_id)
        prefix = f"{epoch_stamp}{checkout_digest}{worker_code}"
        tail_width = namespace_constants.NAMESPACE_TOKEN_LENGTH - len(prefix)
        tail = FlextTestsNamespaceUtilitiesMixin._monotonic_tail(issued_ms, tail_width)
        run_digest = hashlib.sha256(testrun_uid.encode(encoding="utf-8")).hexdigest()[
            :6
        ]
        return m.Tests.TestNamespace(
            token=f"{prefix}{tail}",
            run_token=f"{checkout_digest}{run_digest}",
            worker=worker_id,
            checkout=checkout_digest,
            issued_at_ns=time.time_ns(),
            root=str(checkout_root),
        )

    @classmethod
    def _monotonic_tail(cls, issued_ms: int, width: int) -> str:
        """Return a ``width``-digit base36 tail unique within this process.

        Raises:
            OverflowError: If namespace tail space exhausted within.
        """
        space = len(FlextTestsConstantsNamespace.NAMESPACE_BASE36_ALPHABET) ** width
        with cls._issue_lock:
            last = cls._last_issue
            if last is not None and last[0] >= issued_ms:
                stamp_ms, value = last[0], last[1] + 1
                if value >= space:
                    msg = f"namespace tail space exhausted within {stamp_ms} ms"
                    raise OverflowError(msg)
            else:
                stamp_ms, value = issued_ms, secrets.randbelow(space // 2)
            cls._last_issue = (stamp_ms, value)
        return cls._base36(value).rjust(
            width,
            FlextTestsConstantsNamespace.NAMESPACE_BASE36_ALPHABET[0],
        )

    @staticmethod
    def _base36(value: int) -> str:
        """Encode a non-negative integer as lowercase base36.

        Returns:
            The resulting ``str``.
        """
        alphabet = FlextTestsConstantsNamespace.NAMESPACE_BASE36_ALPHABET
        if value == 0:
            return alphabet[0]
        encoded: list[str] = []
        while value:
            value, remainder = divmod(value, len(alphabet))
            encoded.append(alphabet[remainder])
        return "".join(reversed(encoded))

    @staticmethod
    def _worker_code(worker_id: str) -> str:
        """Condense a worker identifier to two lowercase base36 digits.

        Returns:
            The resulting ``str``.
        """
        alphabet = FlextTestsConstantsNamespace.NAMESPACE_BASE36_ALPHABET
        digest = hashlib.sha256(worker_id.encode(encoding="utf-8")).hexdigest()
        width = FlextTestsConstantsNamespace.NAMESPACE_WORKER_CODE_LENGTH
        return "".join(
            alphabet[int(digest[index * 8 : (index + 1) * 8], 16) % len(alphabet)]
            for index in range(width)
        )


__all__: list[str] = ["FlextTestsNamespaceUtilitiesMixin"]
