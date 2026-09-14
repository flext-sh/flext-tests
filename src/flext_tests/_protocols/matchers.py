"""Callable contracts over owned matcher payloads."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Iterable

    from flext_tests import p


class FlextTestsMatchersProtocolsMixin:
    """Structural matcher capabilities without recursive type aliases."""

    @runtime_checkable
    class PayloadPredicate(Protocol):
        """Evaluate a validated native payload."""

        def __call__(self, value: p.Tests.Payload, /) -> bool: ...

    @runtime_checkable
    class PayloadSortKey(Protocol):
        """Extract a comparable owned value from a payload."""

        def __call__(self, value: p.Tests.Payload, /) -> p.Tests.Payload: ...

    class DeepPredicate(Protocol):
        """Read path expectations without serializing their native leaves."""

        def items(self) -> Iterable[
            tuple[str, p.Tests.Payload | FlextTestsMatchersProtocolsMixin.PayloadPredicate]
        ]: ...


__all__: list[str] = ["FlextTestsMatchersProtocolsMixin"]
