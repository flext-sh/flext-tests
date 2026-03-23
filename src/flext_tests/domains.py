"""Test domain objects and fixtures for FLEXT ecosystem tests.

Provides reusable domain objects, test data structures, and fixtures for
domain-specific testing scenarios. Includes payloads, API responses,
validation test cases, and domain result helpers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import uuid
from collections.abc import Mapping, MutableMapping, Sequence

from flext_tests import m, t


class FlextTestsDomains:
    """Test domain objects and fixtures.

    Provides common test data and domain objects used across FLEXT test suites.
    """

    @staticmethod
    def build_dbt_project_config(
        *,
        name: str,
        version: str,
        profile: str,
        model_config: Mapping[str, t.Tests.Testobject],
        variables: Mapping[str, t.Tests.Testobject],
    ) -> Mapping[str, t.Tests.Testobject]:
        """Create a shared dbt project configuration structure."""
        return {
            "name": name,
            "version": version,
            "profile": profile,
            "model-paths": ["models"],
            "analysis-paths": ["analyses"],
            "test-paths": ["tests"],
            "seed-paths": ["seeds"],
            "macro-paths": ["macros"],
            "snapshot-paths": ["snapshots"],
            "docs-paths": ["docs"],
            "asset-paths": ["assets"],
            "target-path": "target",
            "clean-targets": ["target", "dbt_packages"],
            "require-dbt-version": ">=1.8.0",
            "model_config": dict(model_config.items()),
            "vars": dict(variables.items()),
        }

    @staticmethod
    def default_handler_case_specs() -> Sequence[Mapping[str, t.Tests.Testobject]]:
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
    def api_response_data(
        status: str = "success",
        *,
        include_data: bool | None = None,
        **custom_fields: t.Tests.Testobject,
    ) -> MutableMapping[str, t.Tests.Testobject]:
        """Create API response test data.

        Args:
            status: Response status
            include_data: Whether to include data field
            **custom_fields: Custom response fields

        Returns:
            API response dictionary

        """
        response: MutableMapping[str, t.Tests.Testobject] = {
            "status": status,
            "timestamp": "2025-01-01T00:00:00Z",
            "request_id": str(uuid.uuid4()),
        }
        if include_data:
            response["data"] = {"test": "data"}
        if status == "error":
            response["error"] = {"code": "TEST_ERROR", "message": "Test error message"}
        response.update(custom_fields)
        return response

    @staticmethod
    def create_configuration(
        service_type: str = "api",
        environment: str = "test",
        **overrides: t.Tests.Testobject,
    ) -> MutableMapping[str, t.Tests.Testobject]:
        """Create test configuration data using factories.

        Args:
            service_type: Type of service configuration
            environment: Environment setting
            **overrides: Additional configuration overrides

        Returns:
            Configuration dictionary

        """
        config_result = m.Tests.Config(
            service_type=service_type,
            environment=environment,
        )
        base_config: MutableMapping[str, t.Tests.Testobject] = {
            "service_type": getattr(config_result, "service_type", service_type),
            "environment": getattr(config_result, "environment", environment),
            "debug": getattr(config_result, "debug", False),
            "log_level": getattr(config_result, "log_level", "INFO"),
            "timeout": getattr(config_result, "timeout", 30.0),
            "max_retries": getattr(config_result, "max_retries", 3),
            "namespace": f"test_{service_type}_{uuid.uuid4().hex[:8]}",
            "storage_backend": "memory",
            "enable_caching": True,
            "cache_ttl": 300,
        }
        base_config.update(overrides)
        return base_config

    @staticmethod
    def create_payload(
        data_type: str = "user",
        **custom_fields: t.Tests.Testobject,
    ) -> MutableMapping[str, t.Tests.Testobject]:
        """Create test payload data.

        Args:
            data_type: Type of data to create
            **custom_fields: Custom field overrides

        Returns:
            Payload dictionary

        """
        payloads: MutableMapping[str, Mapping[str, t.Tests.Testobject]] = {
            "user": {
                "id": str(uuid.uuid4()),
                "name": "Test User",
                "email": "test@example.com",
                "active": True,
            },
            "order": {
                "order_id": str(uuid.uuid4()),
                "user_id": str(uuid.uuid4()),
                "amount": 99.99,
                "currency": "USD",
                "status": "pending",
            },
            "api_request": {
                "method": "GET",
                "url": "/api/test",
                "headers": {"Content-Type": "application/json"},
                "body": None,
            },
        }
        payload = dict(payloads.get(data_type, {}).items())
        payload.update(custom_fields)
        return payload

    @staticmethod
    def create_service(
        service_type: str = "api",
        **config: t.Tests.Testobject,
    ) -> MutableMapping[str, t.Tests.Testobject]:
        """Create test service configuration.

        Args:
            service_type: Type of service
            **config: Service configuration

        Returns:
            Service configuration dictionary

        """
        base_service: MutableMapping[str, t.Tests.Testobject] = {
            "type": service_type,
            "name": f"test_{service_type}_service",
            "enabled": True,
            "config": FlextTestsDomains.create_configuration(service_type=service_type),
        }
        base_service.update(config)
        return base_service

    @staticmethod
    def create_user(**overrides: str | bool) -> MutableMapping[str, str | bool]:
        """Create test user data using factories.

        Args:
            **overrides: User field overrides

        Returns:
            User data dictionary

        """
        first_name = str(overrides.get("first_name", "Test"))
        last_name = str(overrides.get("last_name", "User"))
        email = str(overrides.get("email", "test@example.com"))
        user_model_result = m.Tests.User(
            id="",
            name=f"{first_name} {last_name}",
            email=email,
        )
        user: MutableMapping[str, str | bool] = {
            "id": getattr(user_model_result, "id", ""),
            "username": str(overrides.get("username", "testuser")),
            "email": getattr(user_model_result, "email", email),
            "first_name": first_name,
            "last_name": last_name,
            "active": getattr(user_model_result, "active", True),
            "created_at": "2025-01-01T00:00:00Z",
            "updated_at": "2025-01-01T00:00:00Z",
        }
        user.update(overrides)
        return user

    @staticmethod
    def valid_email_cases() -> Sequence[tuple[str, bool]]:
        """Get valid email test cases.

        Returns:
            List of (email, is_valid) tuples

        """
        return [
            ("test@example.com", True),
            ("user.name@domain.co.uk", True),
            ("test+tag@example.com", True),
            ("invalid-email", False),
            ("@example.com", False),
            ("test@", False),
            ("", False),
        ]


td = FlextTestsDomains

__all__ = ["FlextTestsDomains", "td"]
