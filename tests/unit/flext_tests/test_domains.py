"""Unit tests for flext_tests.domains module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import operator

from flext_tests import tm
from flext_tests.domains import td
from tests import u


class TestFlextTestsDomains:
    """Test suite for td class."""

    def test_create_configuration_default(self) -> None:
        """Test create_configuration with default parameters."""
        config = td.create_configuration()
        tm.that(isinstance(config, dict), eq=True)
        tm.that(config["service_type"] == "api", eq=True)
        tm.that(config["environment"] == "test", eq=True)
        tm.that(config["debug"] is True, eq=True)
        tm.that(config["log_level"] == "DEBUG", eq=True)
        tm.that(config["timeout"] == 30, eq=True)
        tm.that(config["max_retries"] == 3, eq=True)
        tm.that(config["storage_backend"] == "memory", eq=True)
        tm.that(config["enable_caching"] is True, eq=True)
        tm.that(config["cache_ttl"] == 300, eq=True)
        tm.that("namespace" in config, eq=True)

    def test_create_configuration_custom(self) -> None:
        """Test create_configuration with custom parameters."""
        config = td.create_configuration(
            service_type="database",
            environment="production",
            custom_field="custom_value",
        )
        tm.that(config["service_type"] == "database", eq=True)
        tm.that(config["environment"] == "production", eq=True)
        tm.that(config["custom_field"] == "custom_value", eq=True)

    def test_create_payload_user_default(self) -> None:
        """Test create_payload with user data type default."""
        payload = td.create_payload()
        tm.that(isinstance(payload, dict), eq=True)
        tm.that("id" in payload, eq=True)
        tm.that(payload["name"] == "Test User", eq=True)
        tm.that(payload["email"] == "test@example.com", eq=True)
        tm.that(payload["active"] is True, eq=True)

    def test_create_payload_order(self) -> None:
        """Test create_payload with order data type."""
        payload = td.create_payload("order")
        tm.that(isinstance(payload, dict), eq=True)
        tm.that("order_id" in payload, eq=True)
        tm.that("user_id" in payload, eq=True)
        amount = payload["amount"]
        tm.that(isinstance(amount, float), eq=True)
        tm.that(abs(amount - 99.99) < 1e-9, eq=True)
        tm.that(payload["currency"] == "USD", eq=True)
        tm.that(payload["status"] == "pending", eq=True)

    def test_create_payload_api_request(self) -> None:
        """Test create_payload with api_request data type."""
        payload = td.create_payload("api_request")
        tm.that(isinstance(payload, dict), eq=True)
        tm.that(payload["method"] == "GET", eq=True)
        tm.that(payload["url"] == "/api/test", eq=True)
        tm.that(payload["headers"] == {"Content-Type": "application/json"}, eq=True)
        tm.that(payload["body"] is None, eq=True)

    def test_create_payload_custom_fields(self) -> None:
        """Test create_payload with custom field overrides."""
        payload = td.create_payload("user", custom_field="custom_value")
        tm.that(payload["custom_field"] == "custom_value", eq=True)
        tm.that(payload["name"] == "Test User", eq=True)

    def test_create_payload_unknown_type(self) -> None:
        """Test create_payload with unknown data type."""
        payload = td.create_payload("unknown")
        tm.that(isinstance(payload, dict), eq=True)
        tm.that(payload == {}, eq=True)

    def test_api_response_data_success_default(self) -> None:
        """Test api_response_data with success status default."""
        response = td.api_response_data()
        tm.that(isinstance(response, dict), eq=True)
        tm.that(response["status"] == "success", eq=True)
        tm.that("timestamp" in response, eq=True)
        tm.that("request_id" in response, eq=True)
        tm.that("data" not in response, eq=True)

    def test_api_response_data_success_with_data(self) -> None:
        """Test api_response_data with success status and data."""
        response = td.api_response_data(
            status="success",
            include_data=True,
        )
        tm.that(response["status"] == "success", eq=True)
        tm.that(response["data"] == {"test": "data"}, eq=True)

    def test_api_response_data_error(self) -> None:
        """Test api_response_data with error status."""
        response = td.api_response_data(status="error")
        tm.that(response["status"] == "error", eq=True)
        tm.that("error" in response, eq=True)
        error_value = response.get("error")
        if isinstance(error_value, dict):
            error_obj = error_value
            tm.that(error_obj.get("code") == "TEST_ERROR", eq=True)
            tm.that(error_obj.get("message") == "Test error message", eq=True)

    def test_api_response_data_custom_fields(self) -> None:
        """Test api_response_data with custom field overrides."""
        response = td.api_response_data(custom_field="custom_value")
        tm.that(response["custom_field"] == "custom_value", eq=True)
        tm.that(response["status"] == "success", eq=True)

    def test_valid_email_cases(self) -> None:
        """Test valid_email_cases returns correct test cases."""
        cases = td.valid_email_cases()
        tm.that(isinstance(cases, list), eq=True)
        tm.that(len(cases) == 7, eq=True)
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
        tm.that("test@example.com" in valid_emails, eq=True)
        tm.that("invalid-email" in invalid_emails, eq=True)
        tm.that("" in invalid_emails, eq=True)

    def test_create_service_default(self) -> None:
        """Test create_service with default parameters."""
        service = td.create_service()
        tm.that(isinstance(service, dict), eq=True)
        tm.that(service["type"] == "api", eq=True)
        tm.that(service["name"] == "test_api_service", eq=True)
        tm.that(service["enabled"] is True, eq=True)
        tm.that("config" in service, eq=True)

    def test_create_service_custom(self) -> None:
        """Test create_service with custom parameters."""
        service = td.create_service(
            "database",
            custom_field="custom_value",
        )
        tm.that(service["type"] == "database", eq=True)
        tm.that(service["name"] == "test_database_service", eq=True)
        tm.that(service["custom_field"] == "custom_value", eq=True)

    def test_create_user_default(self) -> None:
        """Test create_user with default parameters."""
        user = td.create_user()
        tm.that(isinstance(user, dict), eq=True)
        tm.that("id" in user, eq=True)
        tm.that(user["username"] == "testuser", eq=True)
        tm.that(user["email"] == "test@example.com", eq=True)
        tm.that(user["first_name"] == "Test", eq=True)
        tm.that(user["last_name"] == "User", eq=True)
        tm.that(user["active"] is True, eq=True)
        tm.that("created_at" in user, eq=True)
        tm.that("updated_at" in user, eq=True)

    def test_create_user_overrides(self) -> None:
        """Test create_user with field overrides."""
        user = td.create_user(username="customuser", active=False)
        tm.that(user["username"] == "customuser", eq=True)
        tm.that(user["active"] is False, eq=True)
        tm.that(user["email"] == "test@example.com", eq=True)
