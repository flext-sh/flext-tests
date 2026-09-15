"""Domain model extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_core import m


class FlextTestsDomainModelsMixin:
    """Domain-model namespace mixin."""

    class HandlerCaseSpec(m.FrozenModel):
        """Test handler case specification."""

        handler_id: Annotated[str, m.Field(description="Unique handler identifier.")]
        handler_type: Annotated[
            str, m.Field(description="Handler implementation kind.")
        ]
        description: Annotated[str, m.Field(description="Human-readable summary.")]
        expected_result: Annotated[
            str | None, m.Field(description="Expected outcome label.")
        ] = None
        should_fail: Annotated[
            bool, m.Field(description="Whether the case must raise.")
        ] = False
        error_message: Annotated[
            str | None, m.Field(description="Expected error text.")
        ] = None
