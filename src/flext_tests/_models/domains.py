"""Domain model extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import m


class FlextTestsDomainModelsMixin:
    """Domain-model namespace mixin."""

    class HandlerCaseSpec(m.FrozenModel):
        """Test handler case specification."""

        handler_id: str
        handler_type: str
        description: str
        expected_result: str | None = None
        should_fail: bool = False
        error_message: str | None = None
