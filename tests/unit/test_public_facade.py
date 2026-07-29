from __future__ import annotations

from flext_tests import tm


class TestsFlextTestsPublicFacade:
    def test_models_and_utilities_import_together(self) -> None:
        from flext_tests import m, u

        tm.that(m.__name__, eq="flext_tests.models")
        tm.that(u.__name__, eq="flext_tests.utilities")


__all__: list[str] = ["TestsFlextTestsPublicFacade"]
