"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Generator,
)
from contextlib import contextmanager
from unittest.mock import patch

from flext_core import (
    FlextSettings,
)
from flext_tests._typings.base import FlextTestsBaseTypesMixin
from flext_tests.protocols import FlextTestsProtocols as p
from flext_tests.typings import FlextTestsTypes as t


class FlextTestsConfigHelpersUtilitiesMixin:
    """Config testing helpers - use FlextSettings directly when possible."""

    @staticmethod
    def assert_config_fields(
        settings: p.Settings,
        expected_fields: t.MappingKV[str, t.JsonValue],
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
            Test FlextSettings singleton with overrides applied

        """
        settings = FlextSettings.fetch_global()
        if not kwargs:
            return settings
        candidate = settings.model_copy(update=kwargs, deep=True)
        computed_fields = set(type(candidate).model_computed_fields)
        return FlextSettings.model_validate(
            candidate.model_dump(exclude=computed_fields),
        )

    @staticmethod
    @contextmanager
    def env_vars_context(
        env_vars: t.MappingKV[str, FlextTestsBaseTypesMixin.TestobjectSerializable],
        vars_to_clear: t.StrSequence | None = None,
    ) -> Generator[None]:
        """Context manager for temporary environment variable changes."""
        with patch.dict("os.environ", {}, clear=False) as environ:
            for var in vars_to_clear or ():
                environ.pop(var, None)
            environ.update({key: str(value) for key, value in env_vars.items()})
            yield
