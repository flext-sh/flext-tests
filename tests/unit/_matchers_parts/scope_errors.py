"""Private matcher scope and error test mixins."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from flext_tests import r, tm

if TYPE_CHECKING:
    from tests import p


class MatchersScopeErrorsMixin:
    """Matcher scope and error tests."""

    def test_check_returns_chain(self) -> None:
        """Test tm.check() returns Chain t.JsonValue."""
        result = r[int].ok(42)
        chain = tm.check(result)
        tm.that(chain, none=False)

    def test_scope_basic_usage(self) -> None:
        """Test tm.scope() basic usage."""
        with tm.scope() as scope:
            tm.that(scope, none=False)

    def test_scope_with_settings(self) -> None:
        """Test tm.scope() with settings parameter."""
        with tm.scope(settings={"debug": True}) as scope:
            tm.that(scope.settings["debug"] is True, eq=True)

    def test_scope_with_container(self) -> None:
        """Test tm.scope() with container parameter."""
        mock_service = "test_service_value"
        with tm.scope(container={"service": mock_service}) as scope:
            tm.that(scope.container["service"], eq=mock_service)

    def test_scope_with_context(self) -> None:
        """Test tm.scope() with context parameter."""
        with tm.scope(context={"user_id": 123}) as scope:
            tm.that(scope.context["user_id"], eq=123)

    def test_scope_applies_removes_and_restores_real_environment(self) -> None:
        """Environment scope restores both overridden and removed names."""
        present_key = "FLEXT_TEST_SCOPE_PRESENT"
        removed_key = "FLEXT_TEST_SCOPE_REMOVED"
        with tm.scope(env={removed_key: "outer"}):
            with tm.scope(
                env={present_key: "inner"}, remove_env_keys=(removed_key,)
            ):
                tm.that(os.environ[present_key], eq="inner")
                tm.that(removed_key in os.environ, eq=False)
            tm.that(os.environ[removed_key], eq="outer")
            tm.that(present_key in os.environ, eq=False)

    def test_ok_invalid_parameter_type(self) -> None:
        """Test tm.ok() with invalid parameter type raises ValueError."""
        result = r[int].ok(42)
        with pytest.raises(ValueError, match="Parameter validation failed"):
            tm.ok(result, len="invalid")

    def test_fail_invalid_parameter_type(self) -> None:
        """Test tm.fail() with invalid parameter type raises ValueError."""
        result: p.Result[str] = r[str].fail("error")
        with pytest.raises(ValueError, match="Parameter validation failed"):
            tm.fail(result, code=123)

    def test_that_invalid_parameter_type(self) -> None:
        """Test tm.that() with invalid parameter type raises ValueError."""
        with pytest.raises(ValueError, match="Parameter validation failed"):
            tm.that([1, 2, 3], len="invalid")

    def test_scope_invalid_parameter_type(self) -> None:
        """Test tm.scope() with invalid parameter type raises ValueError."""
        with (
            pytest.raises(ValueError, match="Parameter validation failed"),
            tm.scope(env="invalid"),
        ):
            pass
