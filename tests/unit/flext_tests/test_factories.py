"""Unit tests for flext_tests.factories module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

import pytest
from flext_core import r
from pydantic import BaseModel as _BaseModel

from flext_tests import tm, tt
from tests import m, t
from tests.test_utils import assertion_helpers


class TestFactoriesHelpers:
    """Shared aliases and helpers for factory tests."""

    @staticmethod
    def extract_model[T: _BaseModel](
        result: _BaseModel
        | list[_BaseModel]
        | Mapping[str, _BaseModel]
        | r[_BaseModel]
        | r[list[_BaseModel]]
        | r[Mapping[str, _BaseModel]],
        model_type: type[T],
    ) -> T:
        """Extract BaseModel from union type returned by tt.model().

        Args:
            result: Union type from tt.model()
            model_type: Expected concrete model type for type narrowing.

        Returns:
            Instance of the requested model type T.

        Raises:
            AssertionError: If result is not a single BaseModel

        """
        extracted: _BaseModel
        if isinstance(result, r):
            typed_r = cast(
                "r[_BaseModel | list[_BaseModel] | Mapping[str, _BaseModel]]", result
            )
            unwrapped = typed_r.value
            if isinstance(unwrapped, _BaseModel):
                extracted = unwrapped
            elif isinstance(unwrapped, list) and unwrapped:
                extracted = unwrapped[0]
            elif isinstance(unwrapped, Mapping):
                first_value = next(iter(unwrapped.values()), None)
                if isinstance(first_value, _BaseModel):
                    extracted = first_value
                else:
                    msg = f"Expected BaseModel, got {type(unwrapped)}"
                    raise AssertionError(msg)
            else:
                msg = f"Expected BaseModel, got {type(unwrapped)}"
                raise AssertionError(msg)
        elif isinstance(result, _BaseModel):
            extracted = result
        else:
            msg = f"Expected BaseModel, got {type(result)}"
            raise AssertionError(msg)
        if not isinstance(extracted, model_type):
            msg = f"Expected {model_type.__name__}, got {type(extracted).__name__}"
            raise AssertionError(msg)
        return extracted

    @staticmethod
    def as_single_payload_result(
        value: r[t.Tests.object] | list[r[t.Tests.object]],
    ) -> r[t.Tests.object]:
        return value if isinstance(value, r) else value[0]

    @staticmethod
    def as_payload_list(
        value: list[t.Tests.object] | r[list[t.Tests.object]],
    ) -> list[t.Tests.object]:
        return value if isinstance(value, list) else value.value

    @staticmethod
    def as_payload_mapping(
        value: Mapping[str, t.Tests.object] | r[Mapping[str, t.Tests.object]],
    ) -> Mapping[str, t.Tests.object]:
        return value if isinstance(value, Mapping) else value.value


class TestUser:
    """Test suite for User model."""

    def test_user_creation_default(self) -> None:
        """Test User model creation with defaults."""
        user = m.Tests.User(
            id="test-123",
            name="Test User",
            email="test@example.com",
        )
        tm.that(user.id == "test-123", eq=True)
        tm.that(user.name == "Test User", eq=True)
        tm.that(user.email == "test@example.com", eq=True)
        tm.that(user.active is True, eq=True)

    def test_user_creation_with_active(self) -> None:
        """Test User model creation with active flag."""
        user = m.Tests.User(
            id="test-123",
            name="Test User",
            email="test@example.com",
            active=False,
        )
        tm.that(user.active is False, eq=True)


class TestConfig:
    """Test suite for Config model."""

    def test_config_creation_default(self) -> None:
        """Test Config model creation with defaults."""
        config = m.Tests.Config()
        tm.that(config.service_type == "api", eq=True)
        tm.that(config.environment == "test", eq=True)
        tm.that(config.debug is True, eq=True)
        tm.that(config.log_level == "DEBUG", eq=True)
        tm.that(config.timeout == 30, eq=True)
        tm.that(config.max_retries == 3, eq=True)

    def test_config_creation_custom(self) -> None:
        """Test Config model creation with custom values."""
        config = m.Tests.Config(
            service_type="database",
            environment="production",
            debug=False,
            timeout=60,
        )
        tm.that(config.service_type == "database", eq=True)
        tm.that(config.environment == "production", eq=True)
        tm.that(config.debug is False, eq=True)
        tm.that(config.timeout == 60, eq=True)


class TestService:
    """Test suite for Service model."""

    def test_service_creation_minimal(self) -> None:
        """Test Service model creation with minimal fields."""
        service = m.Tests.Service(id="test-123")
        tm.that(service.id == "test-123", eq=True)
        tm.that(service.type == "api", eq=True)
        tm.that(service.name == "", eq=True)
        tm.that(service.status == "active", eq=True)

    def test_service_creation_complete(self) -> None:
        """Test Service model creation with all fields."""
        service = m.Tests.Service(
            id="test-123",
            type="database",
            name="Database Service",
            status="inactive",
        )
        tm.that(service.id == "test-123", eq=True)
        tm.that(service.type == "database", eq=True)
        tm.that(service.name == "Database Service", eq=True)
        tm.that(service.status == "inactive", eq=True)


class TestFlextTestsFactoriesModernAPI:
    """Test suite for tt using modern API (tt.model, tt.op, tt.svc)."""

    def test_model_user_default(self) -> None:
        """Test tt.model('user') with default parameters."""
        user_result = tt.model("user")
        user = TestFactoriesHelpers.extract_model(user_result, m.Tests.User)
        tm.that(isinstance(user, m.Tests.User), eq=True)
        tm.that(user.id is not None, eq=True)
        tm.that(user.name == "Test User", eq=True)
        tm.that("@example.com" in user.email, eq=True)
        tm.that(user.active is True, eq=True)

    def test_model_user_custom(self) -> None:
        """Test tt.model('user') with custom parameters."""
        user_result = tt.model(
            "user",
            model_id="custom-123",
            name="Custom User",
            email="custom@test.com",
        )
        user = TestFactoriesHelpers.extract_model(user_result, m.Tests.User)
        tm.that(isinstance(user, m.Tests.User), eq=True)
        tm.that(user.id == "custom-123", eq=True)
        tm.that(user.name == "Custom User", eq=True)
        tm.that(user.email == "custom@test.com", eq=True)

    def test_model_user_with_overrides(self) -> None:
        """Test tt.model('user') with overrides."""
        user_result = tt.model("user", name="Base User", active=False)
        user = TestFactoriesHelpers.extract_model(user_result, m.Tests.User)
        tm.that(isinstance(user, m.Tests.User), eq=True)
        tm.that(user.name == "Base User", eq=True)
        tm.that(user.active is False, eq=True)

    def test_model_config_default(self) -> None:
        """Test tt.model('config') with default parameters."""
        config_result = tt.model("config")
        config = TestFactoriesHelpers.extract_model(config_result, m.Tests.Config)
        tm.that(isinstance(config, m.Tests.Config), eq=True)
        tm.that(config.service_type == "api", eq=True)
        tm.that(config.environment == "test", eq=True)
        tm.that(config.debug is True, eq=True)

    def test_model_config_custom(self) -> None:
        """Test tt.model('config') with custom parameters."""
        config_result = tt.model(
            "config",
            service_type="database",
            environment="production",
            debug=False,
            timeout=60,
        )
        config = TestFactoriesHelpers.extract_model(config_result, m.Tests.Config)
        tm.that(isinstance(config, m.Tests.Config), eq=True)
        tm.that(config.service_type == "database", eq=True)
        tm.that(config.environment == "production", eq=True)
        tm.that(config.debug is False, eq=True)
        tm.that(config.timeout == 60, eq=True)

    def test_model_config_with_overrides(self) -> None:
        """Test tt.model('config') with overrides."""
        config_result = tt.model("config", log_level="INFO", max_retries=5)
        config = TestFactoriesHelpers.extract_model(config_result, m.Tests.Config)
        tm.that(isinstance(config, m.Tests.Config), eq=True)
        tm.that(config.log_level == "INFO", eq=True)
        tm.that(config.max_retries == 5, eq=True)

    def test_model_service_default(self) -> None:
        """Test tt.model('service') with default parameters."""
        service_result = tt.model("service")
        service = TestFactoriesHelpers.extract_model(service_result, m.Tests.Service)
        tm.that(isinstance(service, m.Tests.Service), eq=True)
        tm.that(service.id is not None, eq=True)
        tm.that(service.type == "api", eq=True)
        tm.that("Test api Service" in service.name, eq=True)
        tm.that(service.status == "active", eq=True)

    def test_model_service_custom(self) -> None:
        """Test tt.model('service') with custom parameters."""
        service_result = tt.model(
            "service",
            service_type="database",
            model_id="custom-123",
            name="Custom Service",
        )
        service = TestFactoriesHelpers.extract_model(service_result, m.Tests.Service)
        tm.that(isinstance(service, m.Tests.Service), eq=True)
        tm.that(service.id == "custom-123", eq=True)
        tm.that(service.type == "database", eq=True)
        tm.that(service.name == "Custom Service", eq=True)

    def test_model_service_with_overrides(self) -> None:
        """Test tt.model('service') with overrides."""
        service_result = tt.model("service", status="inactive")
        service = TestFactoriesHelpers.extract_model(service_result, m.Tests.Service)
        tm.that(isinstance(service, m.Tests.Service), eq=True)
        tm.that(service.status == "inactive", eq=True)

    def test_batch_users_default(self) -> None:
        """Test tt.batch('user') with default count."""
        users_result = tt.batch("user")
        users = users_result
        users_typed: list[m.Tests.User] = [
            u for u in users if isinstance(u, m.Tests.User)
        ]
        tm.that(len(users_typed) == 5, eq=True)
        tm.that(all(isinstance(user, m.Tests.User) for user in users_typed), eq=True)
        tm.that(users_typed[0].name == "User 0", eq=True)
        tm.that(users_typed[1].name == "User 1", eq=True)

    def test_batch_users_custom_count(self) -> None:
        """Test tt.batch('user') with custom count."""
        users_result = tt.batch("user", count=3)
        tm.that(isinstance(users_result, list), eq=True)
        users: list[m.Tests.User] = [
            u for u in users_result if isinstance(u, m.Tests.User)
        ]
        tm.that(len(users) == 3, eq=True)
        tm.that(all(isinstance(user, m.Tests.User) for user in users), eq=True)

    def test_op_simple(self) -> None:
        """Test tt.op('simple') operation."""
        operation = tt.op("simple")
        tm.that(callable(operation), eq=True)
        result = operation()
        tm.that(result == "success", eq=True)

    def test_op_add(self) -> None:
        """Test tt.op('add') operation."""
        operation = tt.op("add")
        tm.that(callable(operation), eq=True)
        result = operation(2, 3)
        tm.that(result == 5, eq=True)

    def test_op_format(self) -> None:
        """Test tt.op('format') operation."""
        operation = tt.op("format")
        tm.that(callable(operation), eq=True)
        result = operation("name", value=20)
        tm.that(result == "name: 20", eq=True)

    def test_op_error(self) -> None:
        """Test tt.op('error') operation."""
        operation = tt.op("error", error_message="Custom error")
        tm.that(callable(operation), eq=True)
        with pytest.raises(ValueError, match="Custom error"):
            operation()

    def test_op_type_error(self) -> None:
        """Test tt.op('type_error') operation."""
        operation = tt.op("type_error", error_message="Type mismatch")
        tm.that(callable(operation), eq=True)
        with pytest.raises(TypeError, match="Type mismatch"):
            operation()

    def test_svc_default(self) -> None:
        """Test tt.svc() with default type."""
        service_class = tt.svc()
        service = service_class()
        tm.that(service.name is None, eq=True)
        tm.that(service.amount is None, eq=True)
        tm.that(service.enabled is None, eq=True)
        result = service.execute()
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == {"service_type": "test"}, eq=True)

    def test_svc_user(self) -> None:
        """Test tt.svc('user') with 'user' type."""
        service_class = tt.svc("user")
        service = service_class()
        result = service.execute()
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that("user_id" in result.value, eq=True)
        tm.that(result.value["user_id"] == "test_123", eq=True)

    def test_svc_user_with_default(self) -> None:
        """Test tt.svc('user') with 'user' type and default flag."""
        service_class = tt.svc("user", default=True)
        service = service_class()
        result = service.execute()
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value["user_id"] == "default_123", eq=True)

    def test_svc_complex_valid(self) -> None:
        """Test tt.svc('complex') with valid data."""
        service_class = tt.svc("complex")
        service = service_class(name="Test", amount=100, enabled=True)
        result = service.execute()
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == {"result": "success"}, eq=True)

    def test_svc_complex_empty_name(self) -> None:
        """Test tt.svc('complex') with empty name."""
        service_class = tt.svc("complex")
        service = service_class(name="")
        result = service.execute()
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("Name is required" in result.error, eq=True)

    def test_svc_complex_negative_amount(self) -> None:
        """Test tt.svc('complex') with negative amount."""
        service_class = tt.svc("complex")
        service = service_class(amount=-10)
        result = service.execute()
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("Amount must be non-negative" in result.error, eq=True)

    def test_svc_complex_disabled_with_amount(self) -> None:
        """Test tt.svc('complex') disabled with amount."""
        service_class = tt.svc("complex")
        service = service_class(enabled=False, amount=100)
        result = service.execute()
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("Cannot have amount when disabled" in result.error, eq=True)

    def test_svc_validate_business_rules_complex_valid(self) -> None:
        """Test validate_business_rules for complex service with valid data."""
        service_class = tt.svc("complex")
        service = service_class(name="Test", amount=100, enabled=True)
        result = service.validate_business_rules()
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value is True, eq=True)

    def test_svc_validate_business_rules_complex_invalid(self) -> None:
        """Test validate_business_rules for complex service with invalid data."""
        service_class = tt.svc("complex")
        service = service_class(name="")
        result = service.validate_business_rules()
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("Name is required" in result.error, eq=True)

    def test_svc_validate_config_complex_valid(self) -> None:
        """Test validate_config for complex service with valid data."""
        service_class = tt.svc("complex")
        service = service_class(name="Test", amount=100)
        result = service.validate_config()
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value is True, eq=True)

    def test_svc_validate_config_name_too_long(self) -> None:
        """Test validate_config for complex service with name too long."""
        service_class = tt.svc("complex")
        long_name = "a" * 51
        service = service_class(name=long_name)
        result = service.validate_config()
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("Name too long" in result.error, eq=True)

    def test_svc_validate_config_amount_too_large(self) -> None:
        """Test validate_config for complex service with amount too large."""
        service_class = tt.svc("complex")
        service = service_class(amount=1001)
        result = service.validate_config()
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("Value too large" in result.error, eq=True)

    def test_svc_validate_config_non_complex(self) -> None:
        """Test validate_config for non-complex service."""
        service_class = tt.svc("test")
        service = service_class()
        result = service.validate_config()
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value is True, eq=True)

    def test_svc_validate_business_rules_non_complex(self) -> None:
        """Test validate_business_rules for non-complex service."""
        service_class = tt.svc("test")
        service = service_class()
        result = service.validate_business_rules()
        tm.that(isinstance(result, r), eq=True)


class TestsFlextTestsFactoriesModel:
    """Tests for tt.model() unified method."""

    def test_model_user_default(self) -> None:
        """Test user model creation with defaults."""
        user_result = tt.model("user")
        user = TestFactoriesHelpers.extract_model(user_result, m.Tests.User)
        tm.that(isinstance(user, m.Tests.User), eq=True)
        tm.that(user.id is not None, eq=True)
        tm.that(user.name == "Test User", eq=True)
        tm.that("@example.com" in user.email, eq=True)
        tm.that(user.active is True, eq=True)

    def test_model_user_custom(self) -> None:
        """Test user model creation with custom parameters."""
        user_result = tt.model("user", name="Custom User", email="custom@test.com")
        user = TestFactoriesHelpers.extract_model(user_result, m.Tests.User)
        tm.that(isinstance(user, m.Tests.User), eq=True)
        tm.that(user.name == "Custom User", eq=True)
        tm.that(user.email == "custom@test.com", eq=True)

    def test_model_batch(self) -> None:
        """Test batch model creation."""
        users = tt.model("user", count=5)
        tm.that(isinstance(users, list), eq=True)
        tm.that(len(users) == 5, eq=True)
        tm.that(all(isinstance(user, m.Tests.User) for user in users), eq=True)

    def test_model_as_result(self) -> None:
        """Test model wrapped in r."""
        result = tt.model("user", as_result=True)
        tm.that(isinstance(result, r), eq=True)
        typed_result = cast("r[_BaseModel]", result)
        _ = assertion_helpers.assert_flext_result_success(typed_result)
        tm.that(isinstance(typed_result.value, m.Tests.User), eq=True)

    def test_model_as_dict(self) -> None:
        """Test model returned as dict."""
        users_dict = tt.model("user", count=3, as_dict=True)
        tm.that(isinstance(users_dict, dict), eq=True)
        tm.that(len(users_dict) == 3, eq=True)
        tm.that(all(isinstance(v, m.Tests.User) for v in users_dict.values()), eq=True)

    def test_model_config(self) -> None:
        """Test config model creation."""
        config = tt.model("config", environment="production")
        tm.that(isinstance(config, m.Tests.Config), eq=True)
        tm.that(config.environment == "production", eq=True)

    def test_model_service(self) -> None:
        """Test service model creation."""
        service_result = tt.model("service", service_type="database")
        service = TestFactoriesHelpers.extract_model(service_result, m.Tests.Service)
        tm.that(isinstance(service, m.Tests.Service), eq=True)
        tm.that(service.type == "database", eq=True)

    def test_model_entity(self) -> None:
        """Test entity model creation."""
        entity = tt.model("entity", name="Test Entity", value=42)
        tm.that(isinstance(entity, m.Tests.Entity), eq=True)
        tm.that(entity.name == "Test Entity", eq=True)

    def test_model_value_object(self) -> None:
        """Test value object model creation."""
        value_obj = tt.model("value", data="test_data", value_count=3)
        tm.that(isinstance(value_obj, m.Tests.Value), eq=True)
        tm.that(value_obj.data == "test_data", eq=True)

    def test_model_with_transform(self) -> None:
        """Test model creation with transform function."""

        def transform_user(value: t.Tests.TestResultValue) -> m.Tests.User:
            if not isinstance(value, m.Tests.User):
                msg = f"Expected User, got {type(value)}"
                raise TypeError(msg)
            return m.Tests.User(
                id=value.id,
                name="Transformed",
                email=value.email,
                active=value.active,
            )

        user_result = tt.model(
            "user",
            name="Original",
            transform=cast(
                "t.Tests.TestResultValue",
                transform_user,
            ),
        )
        user = TestFactoriesHelpers.extract_model(user_result, m.Tests.User)
        tm.that(isinstance(user, m.Tests.User), eq=True)
        tm.that(user.name == "Transformed", eq=True)

    def test_model_with_validate(self) -> None:
        """Test model creation with validation."""

        def validate_active_user(value: t.Tests.TestResultValue) -> bool:
            if not isinstance(value, m.Tests.User):
                return False
            return value.active

        user_result = tt.model(
            "user",
            active=True,
            validate=cast(
                "t.Tests.TestResultValue",
                validate_active_user,
            ),
        )
        user = TestFactoriesHelpers.extract_model(user_result, m.Tests.User)
        tm.that(isinstance(user, m.Tests.User), eq=True)
        tm.that(user.active is True, eq=True)
        result_raw = tt.model(
            "user",
            active=False,
            validate=cast(
                "t.Tests.TestResultValue",
                validate_active_user,
            ),
            as_result=True,
        )
        if isinstance(result_raw, r):
            result_typed: r[_BaseModel] = cast("r[_BaseModel]", result_raw)
        elif isinstance(result_raw, _BaseModel):
            msg = f"Expected r[BaseModel], got BaseModel: {type(result_raw)}"
            raise AssertionError(msg)
        else:
            msg = f"Expected r[BaseModel], got {type(result_raw)}"
            raise AssertionError(msg)
        tm.that(isinstance(result_typed, r), eq=True)
        tm.that(result_typed.is_failure, eq=True)


class TestsFlextTestsFactoriesRes:
    """Tests for tt.res() unified method."""

    def test_res_ok(self) -> None:
        """Test successful result creation."""
        result_raw = tt.res("ok", value=42)
        result = cast(
            "r[int]",
            TestFactoriesHelpers.as_single_payload_result(result_raw),
        )
        tm.that(isinstance(result, r), eq=True)
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == 42, eq=True)

    def test_res_fail(self) -> None:
        """Test failed result creation."""
        result_raw = tt.res("fail", error="Error message")
        result = TestFactoriesHelpers.as_single_payload_result(result_raw)
        tm.that(isinstance(result, r), eq=True)
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that(result.error == "Error message", eq=True)

    def test_res_fail_with_code(self) -> None:
        """Test failed result creation with error code."""
        result_raw = tt.res("fail", error="Error message", error_code="ERR001")
        result = TestFactoriesHelpers.as_single_payload_result(result_raw)
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that(result.error == "Error message", eq=True)

    def test_res_from_value_success(self) -> None:
        """Test from_value with non-None value."""
        result_raw = tt.res("from_value", value=42)
        result = cast(
            "r[int]",
            TestFactoriesHelpers.as_single_payload_result(result_raw),
        )
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == 42, eq=True)

    def test_res_from_value_none(self) -> None:
        """Test from_value with None value."""
        result_raw = tt.res("from_value", value=None, error_on_none="Value is required")
        result = TestFactoriesHelpers.as_single_payload_result(result_raw)
        _ = assertion_helpers.assert_flext_result_failure(result)
        error_msg = result.error or ""
        tm.that("required" in error_msg.lower(), eq=True)

    def test_res_batch_values(self) -> None:
        """Test batch result creation from values."""
        results_raw = tt.res("ok", values=[1, 2, 3])
        results = cast(
            "list[r[int]]",
            results_raw if isinstance(results_raw, list) else [results_raw],
        )
        tm.that(isinstance(results, list), eq=True)
        tm.that(len(results) == 3, eq=True)
        tm.that(all(result.is_success for result in results), eq=True)
        tm.that([result.value for result in results] == [1, 2, 3], eq=True)

    def test_res_batch_errors(self) -> None:
        """Test batch result creation from errors."""
        results_raw = tt.res("fail", errors=["err1", "err2"])
        results = results_raw if isinstance(results_raw, list) else [results_raw]
        tm.that(isinstance(results, list), eq=True)
        tm.that(len(results) == 2, eq=True)
        tm.that(all(result.is_failure for result in results), eq=True)

    def test_res_mix_pattern(self) -> None:
        """Test batch result creation with mix pattern."""
        results_raw = tt.res(
            "ok",
            values=[1, 2],
            errors=["e1", "e2"],
            mix_pattern=[True, False, True, False],
        )
        results = cast(
            "list[r[int]]",
            results_raw if isinstance(results_raw, list) else [results_raw],
        )
        tm.that(len(results) == 4, eq=True)
        tm.that(results[0].is_success and results[0].value == 1, eq=True)
        tm.that(results[1].is_failure, eq=True)
        tm.that(results[2].is_success and results[2].value == 2, eq=True)
        tm.that(results[3].is_failure, eq=True)

    def test_res_with_transform(self) -> None:
        """Test result creation with transform function."""

        def double_integer(value: t.Tests.TestResultValue) -> int:
            if not isinstance(value, int):
                msg = f"Expected int, got {type(value)}"
                raise TypeError(msg)
            return value * 2

        result_raw = tt.res(
            "ok",
            value=5,
            transform=cast(
                "t.Tests.TestResultValue",
                double_integer,
            ),
        )
        result = cast(
            "r[int]",
            TestFactoriesHelpers.as_single_payload_result(result_raw),
        )
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == 10, eq=True)


class TestsFlextTestsFactoriesList:
    """Tests for tt.list() method."""

    def test_list_from_model(self) -> None:
        """Test list creation from model kind."""
        users_raw = tt.list("user", count=3)
        users = cast(
            "list[m.Tests.User]",
            TestFactoriesHelpers.as_payload_list(users_raw),
        )
        tm.that(isinstance(users, list), eq=True)
        tm.that(len(users) == 3, eq=True)
        tm.that(all(isinstance(u, m.Tests.User) for u in users), eq=True)

    def test_list_from_callable(self) -> None:
        """Test list creation from callable factory."""
        numbers_raw = tt.list(lambda: 42, count=5)
        numbers = cast(
            "list[int]",
            TestFactoriesHelpers.as_payload_list(numbers_raw),
        )
        tm.that(numbers == [42, 42, 42, 42, 42], eq=True)

    def test_list_from_sequence(self) -> None:
        """Test list creation from sequence."""

        def double_integer(value: t.Tests.TestResultValue) -> int:
            if not isinstance(value, int):
                msg = f"Expected int, got {type(value)}"
                raise TypeError(msg)
            return value * 2

        doubled_raw = tt.list(
            [1, 2, 3],
            transform=cast(
                "t.Tests.TestResultValue",
                double_integer,
            ),
        )
        doubled = cast(
            "list[int]",
            TestFactoriesHelpers.as_payload_list(doubled_raw),
        )
        tm.that(doubled == [2, 4, 6], eq=True)

    def test_list_with_filter(self) -> None:
        """Test list creation with filter."""

        def is_even_integer(value: t.Tests.TestResultValue) -> bool:
            if not isinstance(value, int):
                return False
            return value % 2 == 0

        evens_raw = tt.list(
            [1, 2, 3, 4, 5],
            filter_=cast(
                "t.Tests.TestResultValue",
                is_even_integer,
            ),
        )
        evens = cast(
            "list[int]",
            TestFactoriesHelpers.as_payload_list(evens_raw),
        )
        tm.that(evens == [2, 4], eq=True)

    def test_list_with_unique(self) -> None:
        """Test list creation with uniqueness."""
        items_raw = tt.list([1, 2, 2, 3, 3, 3], unique=True)
        items = cast(
            "list[int]",
            TestFactoriesHelpers.as_payload_list(items_raw),
        )
        tm.that(len(items) == 3, eq=True)
        tm.that(set(items) == {1, 2, 3}, eq=True)

    def test_list_as_result(self) -> None:
        """Test list creation wrapped in result."""
        result_raw = tt.list("user", count=3, as_result=True)
        tm.that(isinstance(result_raw, r), eq=True)
        result = cast("r[list[m.Tests.User]]", result_raw)
        tm.that(isinstance(result, r), eq=True)
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(len(result.value) == 3, eq=True)


class TestsFlextTestsFactoriesDict:
    """Tests for tt.dict_factory() method."""

    def test_dict_from_model(self) -> None:
        """Test dict creation from model kind."""
        users_raw = tt.dict_factory("user", count=3)
        users = cast(
            "dict[str, m.Tests.User]",
            TestFactoriesHelpers.as_payload_mapping(users_raw),
        )
        tm.that(isinstance(users, dict), eq=True)
        tm.that(len(users) == 3, eq=True)
        tm.that(all(isinstance(u, m.Tests.User) for u in users.values()), eq=True)

    def test_dict_with_key_factory(self) -> None:
        """Test dict creation with key factory."""

        def user_key(index: t.Tests.TestResultValue) -> str:
            if not isinstance(index, int):
                msg = f"Expected int index, got {type(index)}"
                raise TypeError(msg)
            return f"user_{index}"

        users_raw = tt.dict_factory(
            "user",
            count=3,
            key_factory=cast(
                "t.Tests.TestResultValue",
                user_key,
            ),
        )
        users = cast(
            "dict[str, m.Tests.User]",
            TestFactoriesHelpers.as_payload_mapping(users_raw),
        )
        tm.that(set(users.keys()) == {"user_0", "user_1", "user_2"}, eq=True)

    def test_dict_with_value_factory(self) -> None:
        """Test dict creation with value factory."""

        def value_factory(key: str) -> m.Tests.User:
            return m.Tests.User(
                id=key,
                name=f"User {key}",
                email=f"{key}@test.com",
            )

        users_raw = tt.dict_factory(
            "user",
            count=2,
            value_factory=cast(
                "t.Tests.TestResultValue",
                value_factory,
            ),
        )
        users = cast(
            "dict[str, m.Tests.User]",
            TestFactoriesHelpers.as_payload_mapping(users_raw),
        )
        tm.that(len(users) == 2, eq=True)

    def test_dict_from_mapping(self) -> None:
        """Test dict creation from existing mapping."""
        existing = {"a": 1, "b": 2}
        merged_raw = tt.dict_factory(existing, merge_with={"c": 3})
        merged = cast(
            "dict[str, int]",
            TestFactoriesHelpers.as_payload_mapping(merged_raw),
        )
        tm.that(merged == {"a": 1, "b": 2, "c": 3}, eq=True)

    def test_dict_as_result(self) -> None:
        """Test dict creation wrapped in result."""
        result_raw = tt.dict_factory("user", count=3, as_result=True)
        tm.that(isinstance(result_raw, r), eq=True)
        result = cast("r[dict[str, m.Tests.User]]", result_raw)
        tm.that(isinstance(result, r), eq=True)
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(len(result.value) == 3, eq=True)


class TestsFlextTestsFactoriesGeneric:
    """Tests for tt.generic() method."""

    def test_generic_simple(self) -> None:
        """Test generic type instantiation."""

        class SimpleClass:
            def __init__(self, name: str) -> None:
                self.name = name

        obj = tt.generic(SimpleClass, kwargs={"name": "test"})
        tm.that(isinstance(obj, SimpleClass), eq=True)
        tm.that(obj.name == "test", eq=True)

    def test_generic_with_args(self) -> None:
        """Test generic type instantiation with positional args."""

        class ArgsClass:
            def __init__(self, a: int, b: int, c: str = "default") -> None:
                self.a = a
                self.b = b
                self.c = c

        obj_result = tt.generic(ArgsClass, args=[1, 2], kwargs={"c": "custom"})
        if isinstance(obj_result, r):
            obj = obj_result.value
        elif isinstance(obj_result, list):
            obj = obj_result[0]
        else:
            obj = obj_result
        tm.that(isinstance(obj, ArgsClass), eq=True)
        tm.that(obj.a == 1, eq=True)
        tm.that(obj.b == 2, eq=True)
        tm.that(obj.c == "custom", eq=True)

    def test_generic_batch(self) -> None:
        """Test batch generic type instantiation."""

        class BatchClass:
            def __init__(self, value: int) -> None:
                self.value = value

        objs = tt.generic(BatchClass, kwargs={"value": 42}, count=5)
        tm.that(isinstance(objs, list), eq=True)
        tm.that(len(objs) == 5, eq=True)
        tm.that(all(isinstance(o, BatchClass) for o in objs), eq=True)
        tm.that(all(o.value == 42 for o in objs), eq=True)

    def test_generic_with_validate(self) -> None:
        """Test generic type instantiation with validation."""

        class ValidatedClass:
            def __init__(self, age: int) -> None:
                self.age = age

        def is_adult(value: t.Tests.TestResultValue) -> bool:
            if not isinstance(value, ValidatedClass):
                return False
            return value.age >= 18

        obj_result = tt.generic(
            ValidatedClass,
            kwargs={"age": 25},
            validate=cast(
                "t.Tests.TestResultValue",
                is_adult,
            ),
        )
        if isinstance(obj_result, r):
            obj = obj_result.value
        elif isinstance(obj_result, list):
            obj = obj_result[0]
        else:
            obj = obj_result
        tm.that(isinstance(obj, ValidatedClass), eq=True)
        tm.that(obj.age == 25, eq=True)
        with pytest.raises(ValueError, match="Validation failed"):
            tt.generic(
                ValidatedClass,
                kwargs={"age": 15},
                validate=cast(
                    "t.Tests.TestResultValue",
                    is_adult,
                ),
            )

    def test_generic_as_result(self) -> None:
        """Test generic type instantiation wrapped in result."""

        class ResultClass:
            def __init__(self, value: str) -> None:
                self.value = value

        result = tt.generic(ResultClass, kwargs={"value": "test"}, as_result=True)
        tm.that(isinstance(result, r), eq=True)
        typed_result = cast("r[ResultClass]", result)
        _ = assertion_helpers.assert_flext_result_success(typed_result)
        tm.that(isinstance(result.value, ResultClass), eq=True)
        tm.that(result.value.value == "test", eq=True)
