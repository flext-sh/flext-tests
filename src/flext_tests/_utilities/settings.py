"""Extracted mixin for flext_tests."""

from __future__ import annotations

import os
from collections.abc import Generator
from contextlib import contextmanager
from typing import Self

from flext_core import FlextSettings, settings
from flext_tests import t


class FlextTestsConfigHelpersUtilitiesMixin(FlextSettings):
    """Config testing helpers - use FlextSettings directly when possible.

    MRO carries ``FlextSettings`` (ENFORCE-042); the class is a namespace
    holder mixin, never instantiated — helpers resolve via the MRO.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton/validation machinery cannot leak into instantiated
    # facade composites (e.g. the ``u`` logging facade).
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        return object.__new__(cls)

    def __init__(self, *args: object, **kwargs: object) -> None:
        _ = self, args, kwargs

    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)

    __eq__ = object.__eq__

    __hash__ = object.__hash__

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
    def env_vars_context[ValueT](
        env_vars: t.MappingKV[str, ValueT] | None = None,
        vars_to_clear: t.StrSequence | None = None,
    ) -> Generator[None]:
        """Apply and atomically restore a real process-environment scope."""
        original_environment = os.environ.copy()
        try:
            for var in vars_to_clear or ():
                os.environ.pop(var, None)
            os.environ.update({
                key: str(value) for key, value in (env_vars or {}).items()
            })
            yield
        finally:
            os.environ.clear()
            os.environ.update(original_environment)
