"""Extracted mixin for flext_tests."""

from __future__ import annotations

from flext_core import p, u


class FlextTestsRegistryHelpersUtilitiesMixin:
    """Registry testing helpers over the canonical registry DSL."""

    @staticmethod
    def create_test_registry() -> p.Registry:
        """Create a test registry instance.

        Returns:
            Canonical registry instance typed as `p.Registry`.

        """
        return u.build_registry()
