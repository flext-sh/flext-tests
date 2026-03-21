"""Unit tests for flext_tests.domains module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import operator

from flext_tests.domains import td
from tests import u


class TestFlextTestsDomains:
    """Test suite for td class."""

    def test_create_configuration_default(self) -> None:
        """Test create_configuration with default parameters."""
        config = td.create_configuration()
        u.Tests.Matchers.that(isinstance(config, dict), eq=True)
        u.Tests.Matchers.that(config["service_type"] == "api", eq=True)
        u.Tests.Matchers.that(config["environment"] == "test", eq=True)
        u.Tests.Matchers.that(config["debug"] is True, eq=True)
        u.Tests.Matchers.that(config["log_level"] == "DEBUG", eq=True)
        u.Tests.Matchers.that(config["timeout"] == 30, eq=True)
        u.Tests.Matchers.that(config["max_retries"] == 3, eq=True)
        u.Tests.Matchers.that(config["storage_backend"] == "memory", eq=True)
        u.Tests.Matchers.that(config["enable_caching"] is True, eq=True)
        u.Tests.Matchers.that(config["cache_ttl"] == 300, eq=True)
        u.Tests.Matchers.that("namespace" in config, eq=True)

    def test_create_configuration_custom(self) -> None:
        """Test create_configuration with custom parameters."""
        config = td.create_configuration(
            service_type="database",
            environment="production",
            custom_field="custom_value",
        )
        u.Tests.Matchers.that(config["service_type"] == "database", eq=True)
        u.Tests.Matchers.that(config["environment"] == "production", eq=True)
        u.Tests.Matchers.that(config["custom_field"] == "custom_value", eq=True)

    def test_create_payload_user_default(self) -> None:
        """Test create_payload with user data type default."""
        payload = td.create_payload()
        u.Tests.Matchers.that(isinstance(payload, dict), eq=True)
        u.Tests.Matchers.that("id" in payload, eq=True)
        u.Tests.Matchers.that(payload["name"] == "Test User", eq=True)
        u.Tests.Matchers.that(payload["email"] == "test@example.com", eq=True)
        u.Tests.Matchers.that(payload["active"] is True, eq=True)

    def test_create_payload_order(self) -> None:
        """Test create_payload with order data type."""
        payload = td.create_payload("order")
        u.Tests.Matchers.that(isinstance(payload, dict), eq=True)
        u.Tests.Matchers.that("order_id" in payload, eq=True)
        u.Tests.Matchers.that("user_id" in payload, eq=True)
        amount = payload["amount"]
        u.Tests.Matchers.that(isinstance(amount, float), eq=True)
        if not isinstance(amount, float):
            raise TypeError(f"Expected float, got {type(amount)}")
        u.Tests.Matchers.that(abs(amount - 99.99) < 1e-9, eq=True)
        u.Tests.Matchers.that(payload["currency"] == "USD", eq=True)
        u.Tests.Matchers.that(payload["status"] == "pending", eq=True)

    def test_create_payload_api_request(self) -> None:
        """Test create_payload with api_request data type."""
        payload = td.create_payload("api_request")
        u.Tests.Matchers.that(isinstance(payload, dict), eq=True)
        u.Tests.Matchers.that(payload["method"] == "GET", eq=True)
        u.Tests.Matchers.that(payload["url"] == "/api/test", eq=True)
        u.Tests.Matchers.that(
            payload["headers"] == {"Content-Type": "application/json"}, eq=True
        )
        u.Tests.Matchers.that(payload["body"] is None, eq=True)

    def test_create_payload_custom_fields(self) -> None:
        """Test create_payload with custom field overrides."""
        payload = td.create_payload("user", custom_field="custom_value")
        u.Tests.Matchers.that(payload["custom_field"] == "custom_value", eq=True)
        u.Tests.Matchers.that(payload["name"] == "Test User", eq=True)

    def test_create_payload_unknown_type(self) -> None:
        """Test create_payload with unknown data type."""
        payload = td.create_payload("unknown")
        u.Tests.Matchers.that(isinstance(payload, dict), eq=True)
        u.Tests.Matchers.that(payload == {}, eq=True)

    def test_api_response_data_success_default(self) -> None:
        """Test api_response_data with success status default."""
        response = td.api_response_data()
        u.Tests.Matchers.that(isinstance(response, dict), eq=True)
        u.Tests.Matchers.that(response["status"] == "success", eq=True)
        u.Tests.Matchers.that("timestamp" in response, eq=True)
        u.Tests.Matchers.that("request_id" in response, eq=True)
        u.Tests.Matchers.that("data" not in response, eq=True)

    def test_api_response_data_success_with_data(self) -> None:
        """Test api_response_data with success status and data."""
        response = td.api_response_data(
            status="success",
            include_data=True,
        )
        u.Tests.Matchers.that(response["status"] == "success", eq=True)
        u.Tests.Matchers.that(response["data"] == {"test": "data"}, eq=True)

    def test_api_response_data_error(self) -> None:
        """Test api_response_data with error status."""
        response = td.api_response_data(status="error")
        u.Tests.Matchers.that(response["status"] == "error", eq=True)
        u.Tests.Matchers.that("error" in response, eq=True)
        error_value = response.get("error")
        if isinstance(error_value, dict):
            error_obj = error_value
            u.Tests.Matchers.that(error_obj.get("code") == "TEST_ERROR", eq=True)
            u.Tests.Matchers.that(
                error_obj.get("message") == "Test error message", eq=True
            )

    def test_api_response_data_custom_fields(self) -> None:
        """Test api_response_data with custom field overrides."""
        response = td.api_response_data(custom_field="custom_value")
        u.Tests.Matchers.that(response["custom_field"] == "custom_value", eq=True)
        u.Tests.Matchers.that(response["status"] == "success", eq=True)

    def test_valid_email_cases(self) -> None:
        """Test valid_email_cases returns correct test cases."""
        cases = td.valid_email_cases()
        u.Tests.Matchers.that(isinstance(cases, list), eq=True)
        u.Tests.Matchers.that(len(cases) == 7, eq=True)
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
        u.Tests.Matchers.that("test@example.com" in valid_emails, eq=True)
        u.Tests.Matchers.that("invalid-email" in invalid_emails, eq=True)
        u.Tests.Matchers.that("" in invalid_emails, eq=True)

    def test_create_service_default(self) -> None:
        """Test create_service with default parameters."""
        service = td.create_service()
        u.Tests.Matchers.that(isinstance(service, dict), eq=True)
        u.Tests.Matchers.that(service["type"] == "api", eq=True)
        u.Tests.Matchers.that(service["name"] == "test_api_service", eq=True)
        u.Tests.Matchers.that(service["enabled"] is True, eq=True)
        u.Tests.Matchers.that("config" in service, eq=True)

    def test_create_service_custom(self) -> None:
        """Test create_service with custom parameters."""
        service = td.create_service(
            "database",
            custom_field="custom_value",
        )
        u.Tests.Matchers.that(service["type"] == "database", eq=True)
        u.Tests.Matchers.that(service["name"] == "test_database_service", eq=True)
        u.Tests.Matchers.that(service["custom_field"] == "custom_value", eq=True)

    def test_create_user_default(self) -> None:
        """Test create_user with default parameters."""
        user = td.create_user()
        u.Tests.Matchers.that(isinstance(user, dict), eq=True)
        u.Tests.Matchers.that("id" in user, eq=True)
        u.Tests.Matchers.that(user["username"] == "testuser", eq=True)
        u.Tests.Matchers.that(user["email"] == "test@example.com", eq=True)
        u.Tests.Matchers.that(user["first_name"] == "Test", eq=True)
        u.Tests.Matchers.that(user["last_name"] == "User", eq=True)
        u.Tests.Matchers.that(user["active"] is True, eq=True)
        u.Tests.Matchers.that("created_at" in user, eq=True)
        u.Tests.Matchers.that("updated_at" in user, eq=True)

    def test_create_user_overrides(self) -> None:
        """Test create_user with field overrides."""
        user = td.create_user(username="customuser", active=False)
        u.Tests.Matchers.that(user["username"] == "customuser", eq=True)
        u.Tests.Matchers.that(user["active"] is False, eq=True)
        u.Tests.Matchers.that(user["email"] == "test@example.com", eq=True)
