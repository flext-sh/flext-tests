"""Extracted mixin for flext_tests."""

from __future__ import annotations

from flext_tests.constants import FlextTestsConstants as c
from flext_tests.models import FlextTestsModels as m


class FlextTestsHandlerHelpersUtilitiesMixin:
    """Helpers for handler testing."""

    @staticmethod
    def create_handler_config(
        handler_id: str,
        handler_name: str,
        handler_type: c.HandlerType | None = None,
        handler_mode: c.HandlerType | None = None,
        command_timeout: int | None = None,
        max_command_retries: int | None = None,
        metadata: m.Metadata | None = None,
    ) -> m.Handler:
        """Create a handler configuration model.

        Args:
            handler_id: Handler identifier
            handler_name: Handler name
            handler_type: Optional handler type (default: COMMAND)
            handler_mode: Optional handler mode (default: type or COMMAND)
            command_timeout: Optional command timeout in seconds
            max_command_retries: Optional max retry count
            metadata: Optional handler metadata

        Returns:
            r[TEntity]: Result containing created entity or error
            Handler configuration model

        """
        h_type = handler_type or c.HandlerType.COMMAND
        h_mode = handler_mode or h_type
        return m.Handler(
            handler_id=handler_id,
            handler_name=handler_name,
            handler_type=h_type,
            handler_mode=h_mode,
            command_timeout=command_timeout or c.DEFAULT_MAX_COMMAND_RETRIES,
            max_command_retries=max_command_retries or c.DEFAULT_MAX_COMMAND_RETRIES,
            metadata=metadata,
        )
