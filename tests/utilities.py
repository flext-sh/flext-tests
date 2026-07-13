"""Utilities for flext-tests tests."""

from __future__ import annotations

from flext_tests import FlextTestsUtilities


class TestsFlextTestsUtilities(FlextTestsUtilities):
    """Utilities for flext-tests tests."""

    class Tests(FlextTestsUtilities.Tests):
        """flext-tests test utilities namespace."""


u = TestsFlextTestsUtilities

__all__: list[str] = ["TestsFlextTestsUtilities", "u"]
