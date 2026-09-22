"""Model declarations for the private file-test package."""

from __future__ import annotations

from tests import m


class TestsFlextTestsFilesModels(m):
    """Inherit shared test models without mixing in test behavior."""


m = TestsFlextTestsFilesModels

__all__: list[str] = ["TestsFlextTestsFilesModels", "m"]
