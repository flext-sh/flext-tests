"""Extracted mixin for flext_tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_tests import c, m


class FlextTestsFlextUtilitiesHandler:
    """Canonical namespace owner."""

    class FlextTestsHandlerHelpersUtilitiesMixin:
        """Helpers for handler testing."""

        @staticmethod
        def create_handler_config(
            handler_id: str,
            handler_name: str,
            options: m.Tests.HandlerConfigParams | None = None,
        ) -> m.Handler:
            """Create a handler configuration model using canonical model defaults.

            Returns:
                The resulting ``m.Handler``.

            """
            params = options if options is not None else m.Tests.HandlerConfigParams()
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
                **(
                    {"metadata": params.metadata} if params.metadata is not None else {}
                ),
            })
            return handler


__all__: list[str] = ["FlextTestsFlextUtilitiesHandler"]
