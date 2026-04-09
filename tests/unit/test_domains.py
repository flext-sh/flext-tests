"""Unit tests for flext_tests.domains module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import operator

from flext_tests import td, tm
from tests import u


class TestFlextTestsDomains:
    """Test suite for td class."""

    def test_create_configuration_default(self) -> None:
        """Test create_configuration with default parameters."""
        config = td.create_configuration()
        tm.that(config, is_=dict)
        tm.that(config["service_type"], eq="api")
        tm.that(config["environment"], eq="test")
        tm.that(config["debug"] is True, eq=True)
        tm.that(config["log_level"], eq="DEBUG")
        tm.that(config["timeout"], eq=30)
        tm.that(config["max_retries"], eq=3)
        tm.that(config["storage_backend"], eq="memory")
        tm.that(config["enable_caching"] is True, eq=True)
        tm.that(config["cache_ttl"], eq=300)
        tm.that(config, has="namespace")

    def test_create_configuration_custom(self) -> None:
        """Test create_configuration with custom parameters."""
        config = td.create_configuration(
            service_type="database",
            environment="production",
            custom_field="custom_value",
        )
        tm.that(config["service_type"], eq="database")
        tm.that(config["environment"], eq="production")
        tm.that(config["custom_field"], eq="custom_value")

    def test_create_payload_user_default(self) -> None:
        """Test create_payload with user data type default."""
        payload = td.create_payload()
        tm.that(payload, is_=dict)
        tm.that(payload, has="id")
        tm.that(payload["name"], eq="Test User")
        tm.that(payload["email"], eq="test@example.com")
        tm.that(payload["active"] is True, eq=True)

    def test_create_payload_order(self) -> None:
        """Test create_payload with order data type."""
        payload = td.create_payload("order")
        tm.that(payload, is_=dict)
        tm.that(payload, has="order_id")
        tm.that(payload, has="user_id")
        amount = payload["amount"]
        tm.that(amount, is_=float)
        if not isinstance(amount, float):
            raise TypeError(f"Expected float, got {type(amount)}")
        tm.that(abs(amount - 99.99), lt=1e-9)
        tm.that(payload["currency"], eq="USD")
        tm.that(payload["status"], eq="pending")

    def test_create_payload_api_request(self) -> None:
        """Test create_payload with api_request data type."""
        payload = td.create_payload("api_request")
        tm.that(payload, is_=dict)
        tm.that(payload["method"], eq="GET")
        tm.that(payload["url"], eq="/api/test")
        tm.that(payload["headers"], eq={"Content-Type": "application/json"})
        tm.that(payload["body"], none=True)

    def test_create_payload_custom_fields(self) -> None:
        """Test create_payload with custom field overrides."""
        payload = td.create_payload("user", custom_field="custom_value")
        tm.that(payload["custom_field"], eq="custom_value")
        tm.that(payload["name"], eq="Test User")

    def test_create_payload_unknown_type(self) -> None:
        """Test create_payload with unknown data type."""
        payload = td.create_payload("unknown")
        tm.that(payload, is_=dict)
        tm.that(payload, eq={})

    def test_api_response_data_success_default(self) -> None:
        """Test api_response_data with success status default."""
        response = td.api_response_data()
        tm.that(response, is_=dict)
        tm.that(response["status"], eq="success")
        tm.that(response, has="timestamp")
        tm.that(response, has="request_id")
        tm.that("data" not in response, eq=True)

    def test_api_response_data_success_with_data(self) -> None:
        """Test api_response_data with success status and data."""
        response = td.api_response_data(
            status="success",
            include_data=True,
        )
        tm.that(response["status"], eq="success")
        tm.that(response["data"], eq={"test": "data"})

    def test_api_response_data_error(self) -> None:
        """Test api_response_data with error status."""
        response = td.api_response_data(status="error")
        tm.that(response["status"], eq="error")
        tm.that(response, has="error")
        error_value = response.get("error")
        if isinstance(error_value, dict):
            assert "code" in error_value and error_value["code"] == "TEST_ERROR"
            assert (
                "message" in error_value
                and error_value["message"] == "Test error message"
            )

    def test_api_response_data_custom_fields(self) -> None:
        """Test api_response_data with custom field overrides."""
        response = td.api_response_data(custom_field="custom_value")
        tm.that(response["custom_field"], eq="custom_value")
        tm.that(response["status"], eq="success")

    def test_valid_email_cases(self) -> None:
        """Test valid_email_cases returns correct test cases."""
        cases = td.valid_email_cases()
        tm.that(cases, is_=list)
        tm.that(len(cases), eq=7)
        valid_emails = list(
            u.map(
                u.filter(cases, operator.itemgetter(1)),
                operator.itemgetter(0),
            ),
        )
        invalid_emails = list(
            u.map(
                u.filter(cases, lambda item: not item[1]),
                operator.itemgetter(0),
            ),
        )
        tm.that(valid_emails, has="test@example.com")
        tm.that(invalid_emails, has="invalid-email")
        tm.that(invalid_emails, has="")

    def test_create_service_default(self) -> None:
        """Test create_service with default parameters."""
        service = td.create_service()
        tm.that(service, is_=dict)
        tm.that(service["type"], eq="api")
        tm.that(service["name"], eq="test_api_service")
        tm.that(service["enabled"] is True, eq=True)
        tm.that(service, has="config")

    def test_create_service_custom(self) -> None:
        """Test create_service with custom parameters."""
        service = td.create_service(
            "database",
            custom_field="custom_value",
        )
        tm.that(service["type"], eq="database")
        tm.that(service["name"], eq="test_database_service")
        tm.that(service["custom_field"], eq="custom_value")

    def test_create_user_default(self) -> None:
        """Test create_user with default parameters."""
        user = td.create_user()
        tm.that(user, is_=dict)
        tm.that(user, has="id")
        tm.that(user["username"], eq="testuser")
        tm.that(user["email"], eq="test@example.com")
        tm.that(user["first_name"], eq="Test")
        tm.that(user["last_name"], eq="User")
        tm.that(user["active"] is True, eq=True)
        tm.that(user, has="created_at")
        tm.that(user, has="updated_at")

    def test_create_user_overrides(self) -> None:
        """Test create_user with field overrides."""
        user = td.create_user(username="customuser", active=False)
        tm.that(user["username"], eq="customuser")
        tm.that(user["active"] is False, eq=True)
        tm.that(user["email"], eq="test@example.com")
