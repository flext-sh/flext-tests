"""Kubernetes (kind) test infrastructure constants for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar


class FlextTestsConstantsKube:
    """Kubernetes (kind) test infrastructure constants mixin."""

    KIND_CONTAINER_NAME: ClassVar[str] = "flext-kind-test"


__all__: list[str] = ["FlextTestsConstantsKube"]
