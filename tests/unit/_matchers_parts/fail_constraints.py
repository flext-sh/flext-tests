"""Private matcher fail constraint test mixins."""

from __future__ import annotations

from flext_tests import tm
from tests import m, p, r


class MatchersFailConstraintsMixin:
    """Matcher fail constraint tests."""

    def test_fail_with_has_parameter(self) -> None:
        """Test tm.fail() with has parameter."""
        result: p.Result[str] = r[str].fail("Database connection failed")
        error = tm.fail(result, has="connection")
        tm.that(error, eq="Database connection failed")

    def test_fail_with_has_sequence_parameter(self) -> None:
        """Test tm.fail() with has sequence parameter."""
        result: p.Result[str] = r[str].fail("Database connection failed")
        error = tm.fail(result, has=["Database", "connection"])
        tm.that(error, eq="Database connection failed")

    def test_fail_with_lacks_parameter(self) -> None:
        """Test tm.fail() with lacks parameter."""
        result: p.Result[str] = r[str].fail("Database error")
        error = tm.fail(result, lacks="internal")
        tm.that(error, eq="Database error")

    def test_fail_with_starts_parameter(self) -> None:
        """Test tm.fail() with starts parameter."""
        result: p.Result[str] = r[str].fail("Error: connection failed")
        error = tm.fail(result, starts="Error:")
        tm.that(error, eq="Error: connection failed")

    def test_fail_with_ends_parameter(self) -> None:
        """Test tm.fail() with ends parameter."""
        result: p.Result[str] = r[str].fail("connection failed")
        error = tm.fail(result, ends="failed")
        tm.that(error, eq="connection failed")

    def test_fail_with_match_parameter(self) -> None:
        """Test tm.fail() with match parameter."""
        result: p.Result[str] = r[str].fail("Error: 404")
        error = tm.fail(result, match="Error: \\d+")
        tm.that(error, eq="Error: 404")

    def test_fail_with_code_parameter(self) -> None:
        """Test tm.fail() with code parameter."""
        result: p.Result[str] = r[str].fail("error", error_code="VALIDATION")
        error = tm.fail(result, code="VALIDATION")
        tm.that(error, eq="error")

    def test_fail_with_code_has_parameter(self) -> None:
        """Test tm.fail() with code_has parameter."""
        result: p.Result[str] = r[str].fail("error", error_code="VALIDATION_ERROR")
        error = tm.fail(result, code_has="VALIDATION")
        tm.that(error, eq="error")

    def test_fail_with_data_parameter(self) -> None:
        """Test tm.fail() with data parameter."""
        result: p.Result[str] = r[str].fail(
            "error",
            error_data=m.ConfigMap(root={"field": "email"}),
        )
        error = tm.fail(result, data={"field": "email"})
        tm.that(error, eq="error")
