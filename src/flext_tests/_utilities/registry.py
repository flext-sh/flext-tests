"""Extracted mixin for flext_tests."""

from __future__ import annotations

from flext_core import (
    FlextRegistry,
)


class FlextTestsRegistryHelpersUtilitiesMixin:
    """Registry testing helpers - use FlextRegistry directly when possible."""

    @staticmethod
    def create_test_registry() -> p.Registry:
        """Create a test registry instance.

        Returns:
            r[TEntity]: Result containing created entity or error
            New FlextRegistry instance

        """
        return FlextRegistry()
