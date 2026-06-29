"""Private matcher validation test mixins."""

from __future__ import annotations

import pytest

from flext_tests import tm
from tests import c, r, t


class MatchersValidationMixin:
    """Matcher validation tests."""

    def test_assert_valid_email_passes(self) -> None:
        """Test tm.that() with email pattern match."""
        tm.that("test@example.com", match=c.Tests.EMAIL_PATTERN_RE)

    def test_assert_valid_email_fails(self) -> None:
        """Test tm.that() with invalid email."""
        with pytest.raises(AssertionError, match="Assertion failed"):
            tm.that("invalid-email", match=c.Tests.EMAIL_PATTERN_RE)

    def test_assert_valid_email_edge_cases(self) -> None:
        """Test tm.that() with various email edge cases."""
        valid_emails = ["user.name@domain.co.uk", "test+tag@example.com", "a@b.co"]
        invalid_emails = ["invalid", "@example.com", "test@", "test.example.com"]
        for email in valid_emails:
            tm.that(email, match=c.Tests.EMAIL_PATTERN_RE)
        for email in invalid_emails:
            with pytest.raises(AssertionError):
                tm.that(email, match=c.Tests.EMAIL_PATTERN_RE)

    def test_assert_settings_valid_passes(self) -> None:
        """Test tm.that() with keys parameter for settings validation."""
        settings = {
            "service_type": "api",
            "environment": "test",
            "timeout": 30,
        }
        tm.that(settings, keys=["service_type", "environment", "timeout"])
        tm.that(settings["timeout"], is_=int, gt=0)

    def test_assert_settings_valid_missing_required_key(self) -> None:
        """Test tm.that() with missing required key."""
        settings = {"service_type": "api"}
        with pytest.raises(AssertionError, match="Missing required keys"):
            tm.that(settings, keys=["service_type", "environment", "timeout"])

    def test_assert_settings_valid_invalid_timeout(self) -> None:
        """Test tm.that() with invalid timeout type."""
        settings = {"service_type": "api", "environment": "test", "timeout": "invalid"}
        with pytest.raises(AssertionError, match="Assertion failed"):
            tm.that(settings["timeout"], is_=int, gt=0)

    def test_assert_settings_valid_zero_timeout(self) -> None:
        """Test tm.that() with zero timeout."""
        settings = {
            "service_type": "api",
            "environment": "test",
            "timeout": 0,
        }
        with pytest.raises(AssertionError, match="Assertion failed"):
            tm.that(settings["timeout"], is_=int, gt=0)

    def test_ok_with_eq_parameter(self) -> None:
        """Test tm.ok() with eq parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, eq=42)
        tm.that(value, eq=42)

    def test_ok_with_eq_parameter_fails(self) -> None:
        """Test tm.ok() with eq parameter fails when value doesn't match."""
        result = r[int].ok(42)
        with pytest.raises(AssertionError):
            tm.ok(result, eq=43)

    def test_ok_with_ne_parameter(self) -> None:
        """Test tm.ok() with ne parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, ne=43)
        tm.that(value, eq=42)

    def test_ok_with_eq_sequence_parameter(self) -> None:
        """Test tm.ok() with structural sequence equality."""
        result = r[t.StrSequence].ok(["a", "b", "c"])
        value = tm.ok(result, eq=["a", "b", "c"])
        tm.that(value, eq=["a", "b", "c"])

    def test_that_with_eq_mapping_parameter(self) -> None:
        """Test tm.that() with structural mapping equality."""
        payload = {
            "service": "api",
            "enabled": True,
            "retries": 2,
        }
        tm.that(payload, eq={"service": "api", "enabled": True, "retries": 2})

    def test_that_with_ne_sequence_parameter_fails(self) -> None:
        """Test tm.that() with structural sequence inequality failure."""
        with pytest.raises(AssertionError, match="did not satisfy constraints"):
            tm.that(["a", "b"], ne=["a", "b"])
