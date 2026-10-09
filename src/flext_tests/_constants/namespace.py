"""Namespace constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar


class FlextTestsConstantsNamespace:
    """Test-namespace token constants."""

    # S105 false positive: this is a regex grammar, not a credential.
    NAMESPACE_TOKEN_PATTERN: ClassVar[str] = r"^[a-z][a-z0-9]{22}$"
    NAMESPACE_TOKEN_LENGTH: ClassVar[int] = 23
    NAMESPACE_BASE36_ALPHABET: ClassVar[str] = "0123456789abcdefghijklmnopqrstuvwxyz"
    """Lowercase base36 digits of every encoded token field."""
    NAMESPACE_CHECKOUT_DIGEST_LENGTH: ClassVar[int] = 8
    NAMESPACE_WORKER_CODE_LENGTH: ClassVar[int] = 2
