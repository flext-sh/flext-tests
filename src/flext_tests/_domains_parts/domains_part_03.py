"""Reusable test case helpers for flext-tests domains."""

from __future__ import annotations

from flext_tests import p, r, t
from flext_tests._domains_parts.domains_part_02 import (
    FlextTestsDomains as FlextTestsDomainsPart02,
)


class FlextTestsDomains(FlextTestsDomainsPart02):
    """Reusable test case helpers."""

    @staticmethod
    def default_handler_case_specs() -> t.SequenceOf[
        t.MappingKV[str, t.Tests.TestobjectSerializable]
    ]:
        """Create shared handler test-case specs for service-base tests."""
        return [
            {
                "handler_id": "success_command",
                "handler_type": "COMMAND",
                "expected_result": "Handled: test",
                "description": "Command handler success",
            },
            {
                "handler_id": "success_query",
                "handler_type": "QUERY",
                "expected_result": "Handled: query",
                "description": "Query handler success",
            },
            {
                "handler_id": "success_event",
                "handler_type": "EVENT",
                "expected_result": "Handled: event",
                "description": "Event handler success",
            },
            {
                "handler_id": "fail_command",
                "handler_type": "COMMAND",
                "should_fail": True,
                "error_message": "Command failed",
                "description": "Command handler failure",
            },
            {
                "handler_id": "fail_query",
                "handler_type": "QUERY",
                "should_fail": True,
                "error_message": "Query failed",
                "description": "Query handler failure",
            },
        ]

    @staticmethod
    def create_result_ok(
        value: t.Tests.TestobjectSerializable,
    ) -> p.Result[t.Tests.TestobjectSerializable]:
        """Create a generic successful result for test flows."""
        return r[t.Tests.TestobjectSerializable].ok(value)

    @staticmethod
    def create_result_failure(
        message: str,
        *,
        error_code: str = "TEST_ERROR",
        error_data: t.JsonMapping | t.ConfigModelInput | None = None,
    ) -> p.Result[t.Tests.TestobjectSerializable]:
        """Create a generic failed result for test flows."""
        return r[t.Tests.TestobjectSerializable].fail(
            message,
            error_code=error_code,
            error_data=error_data,
        )

    @staticmethod
    def valid_email_cases() -> t.SequenceOf[tuple[str, bool]]:
        """Get valid email test cases."""
        return [
            ("test@example.com", True),
            ("user.name@domain.co.uk", True),
            ("test+tag@example.com", True),
            ("invalid-email", False),
            ("@example.com", False),
            ("test@", False),
            ("", False),
        ]


__all__: list[str] = ["FlextTestsDomains"]
