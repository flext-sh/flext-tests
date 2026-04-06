"""Extracted mixin for flext_tests."""

from __future__ import annotations

from collections.abc import (
    Callable,
    MutableMapping,
)
from typing import override

from flext_tests import (
    t,
)


class FlextTestsBadObjectsUtilitiesMixin:
    """Factory for objects that cause errors during testing."""

    class BadModelDump:
        """Object with model_dump that raises."""

        model_dump: Callable[[], MutableMapping[str, t.Tests.Testobject]] = (
            staticmethod(
                lambda: (_ for _ in ()).throw(RuntimeError("Bad model_dump")),
            )
        )

    class BadConfig:
        """Config t.NormalizedValue that raises on attribute access."""

        @override
        def __getattribute__(self, name: str) -> t.Tests.Testobject:
            """Raise error on attribute access - test helper for error testing."""
            if name.startswith("__") and name.endswith("__"):
                result: t.Tests.Testobject = super().__getattribute__(name)
                return result
            msg = f"Bad config: {name}"
            raise AttributeError(msg)

    class BadConfigTypeError:
        """Config t.NormalizedValue that raises TypeError on attribute access."""

        @override
        def __getattribute__(self, name: str) -> t.Tests.Testobject:
            """Raise TypeError on attribute access - test helper for error testing."""
            if name.startswith("__") and name.endswith("__"):
                result: t.Tests.Testobject = super().__getattribute__(name)
                return result
            msg = f"Bad config type: {name}"
            raise TypeError(msg)
