"""Behavioral tests for the public flext-tests service base."""

from __future__ import annotations

from typing import override

from flext_core import r
from flext_tests import p, tm
from flext_tests.base import FlextTestsServiceBase


class TestsFlextTestsServiceBase:
    """Prove the tests service base preserves scalar result types at runtime."""

    class BooleanService(FlextTestsServiceBase[bool]):
        """Service returning a scalar boolean through the canonical tests base."""

        @override
        def execute(self) -> p.Result[bool]:
            """Return a successful boolean result."""
            return r[bool].ok(True)

    def test_boolean_service_executes_through_public_base(self) -> None:
        """A boolean specialization executes without model-only restrictions."""
        result = self.BooleanService().execute()

        tm.that(result.unwrap(), eq=True)
