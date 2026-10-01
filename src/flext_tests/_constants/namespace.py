"""Namespace constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar


class FlextTestsConstantsNamespace:
    """Test-namespace token constants."""

    # S105 false positive: this is a regex grammar, not a credential.
    NAMESPACE_TOKEN_PATTERN: ClassVar[str] = r"^[a-z][a-z0-9]{22}$"  # ruff: ignore[hardcoded-password-string] - regex grammar, not a secret
    NAMESPACE_TOKEN_LENGTH: ClassVar[int] = 23
