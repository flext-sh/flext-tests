"""Private matcher validation test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from copy import deepcopy
from operator import eq
from pathlib import Path

import pytest

from tests import c, m, p, r, t, tm


class TestsFlextTestsMatchersValidationMixin:
    """Matcher validation tests."""

    @staticmethod
    @pytest.mark.parametrize("truth", [True, False])
    @pytest.mark.parametrize("repr_raises", [True, False])
    def test_native_truth_never_formats_the_subject(
        *, truth: bool, repr_raises: bool
    ) -> None:
        """Success and failure evaluate native truth once without representation."""
        events: list[str] = []

        class Subject:
            def __bool__(self) -> bool:
                events.append("bool")
                return truth

            def __repr__(self) -> str:
                events.append("repr")
                if repr_raises:
                    message = "representation must not run"
                    raise ValueError(message)
                return "subject representation"

        subject = Subject()
        result = tm.that(subject, truth=truth)
        tm.that(result, none=True)
        tm.that(events, eq=["bool"])
        with pytest.raises(AssertionError) as raised:
            tm.that(subject, truth=not truth)
        tm.that(raised.value.args, eq=())
        tm.that(events, eq=["bool", "bool"])

    @staticmethod
    @pytest.mark.parametrize("truth", [True, False])
    def test_native_truth_preserves_the_original_bool_exception(*, truth: bool) -> None:
        """A failing bool is the first exception, even when representation raises."""
        events: list[str] = []
        failure = RuntimeError("original bool failure")

        class Subject:
            def __bool__(self) -> bool:
                events.append("bool")
                raise failure

            def __repr__(self) -> str:
                events.append("repr")
                message = "unexpected representation failure"
                raise ValueError(message)

        with pytest.raises(RuntimeError) as raised:
            tm.that(Subject(), truth=truth)
        tm.that(raised.value is failure, truth=True)
        tm.that(events, eq=["bool"])

    @staticmethod
    def test_native_truth_preserves_noncomplementary_comparison_operators() -> None:
        """Expression truth keeps independently defined equality and inequality."""
        events: list[str] = []

        class Subject:
            def __hash__(self) -> int:
                return hash(type(self))

            def __eq__(self, other: p.AttributeProbe) -> bool:
                events.append("eq")
                return self is not other

            def __ne__(self, other: p.AttributeProbe) -> bool:
                events.append("ne")
                return self is not other

        left = Subject()
        right = Subject()
        tm.that(left == right, truth=True)
        tm.that(left != right, truth=True)
        tm.that(events, eq=["eq", "ne"])

    @staticmethod
    def test_native_truth_keeps_callable_messages_as_unevaluated_values() -> None:
        """assertion_message is an assertion argument, not a lazy factory API."""
        events: list[str] = []

        def message(value: p.Tests.NativeMatchValue) -> str:
            events.append("message")
            return str(value)

        tm.that(True, truth=True, assertion_message=message)
        with pytest.raises(AssertionError) as raised:
            tm.that(False, truth=True, assertion_message=message)
        tm.that(raised.value.args[0] is message, truth=True)
        tm.that(events, eq=[])

    @staticmethod
    def test_native_truth_distinguishes_omitted_and_explicit_messages() -> None:
        """Explicit empty/None messages retain their exact AssertionError args."""
        with pytest.raises(AssertionError) as omitted:
            tm.that(False, truth=True)
        tm.that(omitted.value.args, eq=())
        with pytest.raises(AssertionError) as empty:
            tm.that(False, truth=True, msg="")
        tm.that(empty.value.args, eq=("",))
        with pytest.raises(AssertionError) as explicit_none:
            tm.that(False, truth=True, assertion_message=None)
        tm.that(explicit_none.value.args, eq=(None,))
        with pytest.raises(AssertionError) as explicit_empty:
            tm.that(False, truth=True, msg="secondary", assertion_message="")
        tm.that(explicit_empty.value.args, eq=("",))

    @staticmethod
    def test_native_truth_preserves_original_collection_semantics() -> None:
        """Truth checks use Python's original subject without payload conversion."""
        tm.that(["value"], truth=True)
        empty: list[str] = []
        tm.that(empty, truth=False)
        with pytest.raises(AssertionError):
            tm.that(empty, truth=True)
        result = r[int].ok(1)
        tm.ok(result, eq=1)
        # Native equality between a Result and a raw scalar is False; the
        # callable form expresses that cross-type comparison without the
        # statically impossible operator usage pyright rejects.
        with pytest.raises(AssertionError):
            tm.that(eq(result, 1), truth=True)

    @staticmethod
    def test_native_truth_evaluates_failure_message_only_on_failure(
        tmp_path: Path,
    ) -> None:
        """A failure message's real file effect never runs on a passing condition."""
        destination = tmp_path / "assertion-message.txt"

        def failure_message() -> str:
            destination.write_text("failure observed", encoding="utf-8")
            return "native assertion message"

        condition = True
        if not condition:
            tm.that(False, truth=True, assertion_message=failure_message())
        tm.that(destination.exists(), eq=False)
        with pytest.raises(AssertionError, match="native assertion message"):
            tm.that(False, truth=True, assertion_message=failure_message())
        tm.that(destination.read_text(encoding="utf-8"), eq="failure observed")

    @staticmethod
    def test_native_truth_preserves_message_exception_and_empty_message() -> None:
        """Message failures escape unchanged; an empty message remains empty."""
        denominator = len("")
        with pytest.raises(ZeroDivisionError):
            tm.that(False, truth=True, assertion_message=1 / denominator)
        with pytest.raises(AssertionError) as raised:
            tm.that(False, truth=True, assertion_message="")
        tm.that(raised.value.args, eq=("",))

    @staticmethod
    def test_native_truth_rejects_payload_criteria_before_evaluation() -> None:
        """Native truth never silently ignores payload-owned matcher constraints."""
        with pytest.raises(ValueError, match="cannot be combined"):
            tm.that(1, truth=True, eq=1)
        with pytest.raises(ValueError, match="requires the native truth"):
            tm.that(1, assertion_message="unused")

    @staticmethod
    def test_native_matcher_rejects_undeclared_criteria() -> None:
        """A typed operand never opens the matcher to arbitrary option names."""
        with pytest.raises(m.ValidationError):
            tm.that(1, undeclared_criterion=True)

    @staticmethod
    def test_assert_valid_email_passes() -> None:
        """Test tm.that() with email pattern match."""
        tm.that("test@example.com", match=c.Tests.EMAIL_PATTERN_RE)

    @staticmethod
    def test_assert_valid_email_fails() -> None:
        """Test tm.that() with invalid email."""
        with pytest.raises(AssertionError, match="Assertion failed"):
            tm.that("invalid-email", match=c.Tests.EMAIL_PATTERN_RE)

    @staticmethod
    def test_assert_valid_email_edge_cases() -> None:
        """Test tm.that() with various email edge cases."""
        valid_emails = ["user.name@domain.co.uk", "test+tag@example.com", "a@b.co"]
        invalid_emails = ["invalid", "@example.com", "test@", "test.example.com"]
        for email in valid_emails:
            tm.that(email, match=c.Tests.EMAIL_PATTERN_RE)
        for email in invalid_emails:
            with pytest.raises(AssertionError):
                tm.that(email, match=c.Tests.EMAIL_PATTERN_RE)

    @staticmethod
    def test_assert_settings_valid_passes() -> None:
        """Test tm.that() with keys parameter for settings validation."""
        settings = {"service_type": "api", "environment": "test", "timeout": 30}
        tm.that(settings, keys=["service_type", "environment", "timeout"])
        tm.that(settings["timeout"], is_=int, gt=0)

    @staticmethod
    def test_assert_settings_valid_missing_required_key() -> None:
        """Test tm.that() with missing required key."""
        settings = {"service_type": "api"}
        with pytest.raises(AssertionError, match="Missing required keys"):
            tm.that(settings, keys=["service_type", "environment", "timeout"])

    @staticmethod
    def test_assert_settings_valid_invalid_timeout() -> None:
        """Test tm.that() with invalid timeout type."""
        settings = {"service_type": "api", "environment": "test", "timeout": "invalid"}
        with pytest.raises(AssertionError, match="Assertion failed"):
            tm.that(settings["timeout"], is_=int, gt=0)

    @staticmethod
    def test_assert_settings_valid_zero_timeout() -> None:
        """Test tm.that() with zero timeout."""
        settings = {"service_type": "api", "environment": "test", "timeout": 0}
        with pytest.raises(AssertionError, match="Value 0 did not satisfy constraints"):
            tm.that(settings["timeout"], is_=int, gt=0)

    @staticmethod
    def test_ok_with_eq_parameter() -> None:
        """Test tm.ok() with eq parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, eq=42)
        tm.that(value, eq=42)

    @staticmethod
    def test_ok_with_eq_parameter_fails() -> None:
        """Test tm.ok() with eq parameter fails when value doesn't match."""
        result = r[int].ok(42)
        with pytest.raises(AssertionError):
            tm.ok(result, eq=43)

    @staticmethod
    def test_ok_with_ne_parameter() -> None:
        """Test tm.ok() with ne parameter."""
        result = r[int].ok(42)
        value = tm.ok(result, ne=43)
        tm.that(value, eq=42)

    @staticmethod
    def test_ok_with_eq_sequence_parameter() -> None:
        """Test tm.ok() with structural sequence equality."""
        result = r[t.StrSequence].ok(["a", "b", "c"])
        value = tm.ok(result, eq=["a", "b", "c"])
        tm.that(value, eq=["a", "b", "c"])

    @staticmethod
    def test_that_with_eq_mapping_parameter() -> None:
        """Test tm.that() with structural mapping equality."""
        payload = {"service": "api", "enabled": True, "retries": 2}
        tm.that(payload, eq={"service": "api", "enabled": True, "retries": 2})

    @staticmethod
    def test_public_matcher_boundary_accepts_supported_value_shapes() -> None:
        values: tuple[t.JsonValue, ...] = (
            "scalar",
            {"service": "api"},
            ["api", "worker"],
            {"services": ["api", {"workers": [1, 2]}]},
        )
        for value in values:
            tm.that(deepcopy(value), eq=value)
            # Bind the result so ok's payload typevar solves from the family
            # subscript instead of the outer matcher's contextual inference.
            result: p.Result[t.JsonValue] = r[t.JsonValue].ok(value)
            tm.that(tm.ok(result, eq=value), eq=value)

    @staticmethod
    def test_public_matcher_boundary_accepts_approximation() -> None:
        expected = pytest.approx(1.5)
        tm.that(1.5, eq=expected)
        tm.that(tm.ok(r[float].ok(1.5), eq=expected), eq=expected)

    @staticmethod
    def test_that_with_ne_sequence_parameter_fails() -> None:
        """Test tm.that() with structural sequence inequality failure."""
        with pytest.raises(AssertionError, match="did not satisfy constraints"):
            tm.that(["a", "b"], ne=["a", "b"])
