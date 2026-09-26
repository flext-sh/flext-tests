"""Callable contracts over native matcher values."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsMatchersProtocolsMixin(Protocol):
    """Structural matcher capabilities without recursive type aliases."""

    @runtime_checkable
    class MatchPredicate(Protocol):
        """Evaluate the native value a matcher criterion is applied to."""

        def __call__(self, value: t.Tests.NativeMatchValue, /) -> bool: ...


__all__: list[str] = ["FlextTestsMatchersProtocolsMixin"]
