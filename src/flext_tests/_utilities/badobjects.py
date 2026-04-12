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

        model_dump: Callable[
            [], MutableMapping[str, t.Tests.TestobjectSerializable]
        ] = staticmethod(
            lambda: (_ for _ in ()).throw(RuntimeError("Bad model_dump")),
        )

    class BadConfig:
        """Config t.RecursiveContainer that raises on attribute access."""

        @override
        def __getattribute__(self, name: str) -> t.Tests.TestobjectSerializable:
            """Raise error on attribute access - test helper for error testing."""
            if name.startswith("__") and name.endswith("__"):
                result: t.Tests.TestobjectSerializable = super().__getattribute__(name)
                return result
            msg = f"Bad settings: {name}"
            raise AttributeError(msg)

    class BadConfigTypeError:
        """Config t.RecursiveContainer that raises TypeError on attribute access."""

        @override
        def __getattribute__(self, name: str) -> t.Tests.TestobjectSerializable:
            """Raise TypeError on attribute access - test helper for error testing."""
            if name.startswith("__") and name.endswith("__"):
                result: t.Tests.TestobjectSerializable = super().__getattribute__(name)
                return result
            msg = f"Bad settings type: {name}"
            raise TypeError(msg)
