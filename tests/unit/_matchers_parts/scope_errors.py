"""Private matcher scope and error test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

import pytest

from flext_tests import c, r, tm
from tests import m

if TYPE_CHECKING:
    from tests import p


class TestsFlextTestsMatchersScopeErrorsMixin:
    """Matcher scope and error tests."""

    @staticmethod
    def test_check_returns_chain() -> None:
        """tm.check() chains assertions over the result it was given."""
        result = r[int].ok(42)
        chain: m.Tests.Chain[int] = tm.check(result)
        tm.that(chain.result is result, eq=True)

    @staticmethod
    def test_scope_with_settings() -> None:
        """Test tm.scope() with settings parameter."""
        with tm.scope(settings={"debug": True}) as scope:
            tm.that(scope.settings["debug"].atom is True, eq=True)

    @staticmethod
    def test_scope_with_container() -> None:
        """Test tm.scope() with container parameter."""
        mock_service = "test_service_value"
        with tm.scope(container={"service": mock_service}) as scope:
            tm.that(scope.container["service"], eq=mock_service)

    @staticmethod
    def test_scope_with_context() -> None:
        """Test tm.scope() with context parameter."""
        with tm.scope(context={"user_id": 123}) as scope:
            tm.that(scope.context["user_id"], eq=123)

    @staticmethod
    def test_scope_applies_removes_and_restores_real_environment() -> None:
        """Environment scope restores both overridden and removed names."""
        present_key = "FLEXT_TEST_SCOPE_PRESENT"
        removed_key = "FLEXT_TEST_SCOPE_REMOVED"
        with tm.scope(env={removed_key: "outer"}):
            with tm.scope(env={present_key: "inner"}, remove_env_keys=(removed_key,)):
                tm.that(os.environ[present_key], eq="inner")
                tm.that(removed_key in os.environ, eq=False)
            tm.that(os.environ[removed_key], eq="outer")
            tm.that(present_key in os.environ, eq=False)

    @staticmethod
    def test_ok_invalid_parameter_type() -> None:
        """tm.ok() rejects an invalid criterion, naming the offending field."""
        result = r[int].ok(42)
        with pytest.raises(m.ValidationError, match=r"for OkParams\nlen") as error:
            tm.ok(result, len="invalid")
        tm.that({item["loc"][0] for item in error.value.errors()}, eq={"len"})

    @staticmethod
    def test_fail_invalid_parameter_type() -> None:
        """tm.fail() rejects an invalid criterion, naming the offending field."""
        result: p.Result[str] = r[str].fail("error")
        with pytest.raises(m.ValidationError, match=r"for FailParams\ncode") as error:
            tm.fail(result, code=123)
        tm.that({item["loc"][0] for item in error.value.errors()}, eq={"code"})

    @staticmethod
    def test_that_invalid_parameter_type() -> None:
        """tm.that() rejects an invalid criterion, naming the offending field."""
        with pytest.raises(m.ValidationError, match=r"for ThatParams\nlen") as error:
            tm.that([1, 2, 3], len="invalid")
        tm.that({item["loc"][0] for item in error.value.errors()}, eq={"len"})

    @staticmethod
    def test_scope_invalid_parameter_type() -> None:
        """Invalid scope input preserves Pydantic's structured validation error."""
        with pytest.raises(c.ValidationError) as error, tm.scope(env="invalid"):
            pass
        tm.that({item["loc"][0] for item in error.value.errors()}, eq={"env"})
