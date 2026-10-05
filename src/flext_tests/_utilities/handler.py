"""Extracted mixin for flext_tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import u

from flext_tests import c, m


class FlextTestsHandlerConfigParams(m.Value):
    """Optional handler configuration knobs for ``create_handler_config``."""

    handler_type: Annotated[
        c.HandlerType | None,
        u.Field(description="Explicit handler type override."),
    ] = None
    handler_mode: Annotated[
        c.HandlerType | None,
        u.Field(description="Explicit handler mode override."),
    ] = None
    command_timeout: Annotated[
        int | None,
        u.Field(description="Explicit command timeout override."),
    ] = None
    max_command_retries: Annotated[
        int | None,
        u.Field(description="Explicit command retry-count override."),
    ] = None
    metadata: Annotated[
        m.Metadata | None,
        u.Field(description="Explicit handler metadata override."),
    ] = None


class FlextTestsHandlerHelpersUtilitiesMixin:
    """Helpers for handler testing."""

    @staticmethod
    def create_handler_config(
        handler_id: str,
        handler_name: str,
        options: FlextTestsHandlerConfigParams | None = None,
    ) -> m.Handler:
        """Create a handler configuration model using canonical model defaults.

        Returns:
            The resulting ``m.Handler``.
        """
        params = options if options is not None else FlextTestsHandlerConfigParams()
        resolved_handler_type = params.handler_type or c.HandlerType.COMMAND
        handler: m.Handler = m.Handler.model_validate({
            "handler_id": handler_id,
            "handler_name": handler_name,
            "handler_type": resolved_handler_type,
            "handler_mode": params.handler_mode or resolved_handler_type,
            **(
                {"command_timeout": params.command_timeout}
                if params.command_timeout is not None
                else {}
            ),
            **(
                {"max_command_retries": params.max_command_retries}
                if params.max_command_retries is not None
                else {}
            ),
            **({"metadata": params.metadata} if params.metadata is not None else {}),
        })
        return handler
