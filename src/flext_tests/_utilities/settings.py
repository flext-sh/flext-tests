"""Extracted mixin for flext_tests."""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager

from flext_core import FlextSettings, settings
from flext_tests import t


class FlextTestsConfigHelpersUtilitiesMixin:
    """Config testing helpers - use FlextSettings directly when possible."""

    @staticmethod
    def create_test_config(**kwargs: t.Scalar) -> FlextSettings:
        """Create a test settings instance.

        Args:
            **kwargs: Config field values (scalar types: str, int, float, bool, datetime)

        Returns:
            Test FlextSettings singleton with overrides applied

        """
        if not kwargs:
            return settings
        candidate = settings.model_copy(update=kwargs, deep=True)
        computed_fields = set(type(candidate).model_computed_fields)
        return FlextSettings.model_validate(
            candidate.model_dump(exclude=computed_fields)
        )

    @staticmethod
    @contextmanager
    def env_vars_context(
        env_vars: t.MappingKV[str, t.Tests.TestobjectSerializable] | None = None,
        vars_to_clear: t.StrSequence | None = None,
    ) -> Generator[None]:
        """Apply and atomically restore a real process-environment scope."""
        original_environment = os.environ.copy()
        try:
            for var in vars_to_clear or ():
                os.environ.pop(var, None)
            os.environ.update({key: str(value) for key, value in (env_vars or {}).items()})
            yield
        finally:
            os.environ.clear()
            os.environ.update(original_environment)
