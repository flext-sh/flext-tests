"""Extracted mixin for flext_tests."""

from __future__ import annotations

import os
from collections.abc import (
    Generator,
    Mapping,
)
from contextlib import contextmanager

from flext_core import (
    FlextSettings,
)

from flext_tests import (
    p,
    t,
)


class FlextTestsConfigHelpersUtilitiesMixin:
    """Config testing helpers - use FlextSettings directly when possible."""

    @staticmethod
    def assert_config_fields(
        settings: p.Settings,
        expected_fields: Mapping[str, t.JsonValue],
    ) -> None:
        """Assert settings has expected field values.

        Args:
            settings: Config instance to check
            expected_fields: Expected field values

        Raises:
            AssertionError: If fields don't match

        """
        dumped_settings = settings.model_dump()
        for key, expected_value in expected_fields.items():
            actual_value = dumped_settings.get(key)
            msg = f"Config {key}: expected {expected_value}, got {actual_value}"
            assert actual_value == expected_value, msg

    @staticmethod
    def create_test_config(**kwargs: t.Scalar) -> FlextSettings:
        """Create a test settings instance.

        Args:
            **kwargs: Config field values (scalar types: str, int, float, bool, datetime)

        Returns:
            New FlextSettings instance

        """
        scalar_overrides: t.ScalarMapping = dict(kwargs.items())
        return FlextSettings.fetch_global(overrides=scalar_overrides)

    @staticmethod
    @contextmanager
    def env_vars_context(
        env_vars: Mapping[str, t.Tests.TestobjectSerializable],
        vars_to_clear: t.StrSequence | None = None,
    ) -> Generator[None]:
        """Context manager for temporary environment variable changes.

        Args:
            env_vars: Environment variables to set
            vars_to_clear: Variables to clear on entry

        Yields:
            None

        """
        original_values: dict[str, str | None] = {}
        if vars_to_clear:
            for var in vars_to_clear:
                original_values[var] = os.environ.get(var)
                if var in os.environ:
                    del os.environ[var]
        for key, value in env_vars.items():
            if key not in original_values:
                original_values[key] = os.environ.get(key)
            os.environ[key] = str(value)
        try:
            yield
        finally:
            for key, original in original_values.items():
                if original is None:
                    if key in os.environ:
                        del os.environ[key]
                else:
                    os.environ[key] = original
