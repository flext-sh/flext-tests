"""Test matchers and assertions for FLEXT ecosystem tests.

Provides unified assertion API with generalist methods.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import Any, Self

from flext_core import r


class FlextTestsMatchersUtilities:
    class Tests:
        class Matchers:
            @staticmethod
            def ok(result: r[Any], **kwargs: Any) -> Any:
                assert result.is_success, (
                    f"Expected success but got failure: {result.error}"
                )
                val = result.value
                if "eq" in kwargs:
                    assert val == kwargs["eq"], f"Expected {kwargs['eq']}, got {val}"
                if "is_" in kwargs:
                    assert isinstance(val, kwargs["is_"]), (
                        f"Expected instance of {kwargs['is_']}, got {type(val)}"
                    )
                if "contains" in kwargs:
                    assert kwargs["contains"] in val, (
                        f"Expected {val} to contain {kwargs['contains']}"
                    )
                if "length" in kwargs:
                    assert len(val) == kwargs["length"], (
                        f"Expected length {kwargs['length']}, got {len(val)}"
                    )
                return val

            @staticmethod
            def fail(result: r[Any], **kwargs: Any) -> str:
                assert result.is_failure, (
                    f"Expected failure but got success: {result.value}"
                )
                err = result.error
                if "has" in kwargs:
                    expected = kwargs["has"]
                    if isinstance(expected, str):
                        assert expected in err, (
                            f"Expected error to contain '{expected}', got '{err}'"
                        )
                    elif isinstance(expected, list):
                        for exp in expected:
                            assert exp in err, (
                                f"Expected error to contain '{exp}', got '{err}'"
                            )
                if "lacks" in kwargs:
                    expected = kwargs["lacks"]
                    if isinstance(expected, str):
                        assert expected not in err, (
                            f"Expected error to NOT contain '{expected}', got '{err}'"
                        )
                    elif isinstance(expected, list):
                        for exp in expected:
                            assert exp not in err, (
                                f"Expected error to NOT contain '{exp}', got '{err}'"
                            )
                if "match" in kwargs:
                    assert re.search(kwargs["match"], err), (
                        f"Error '{err}' did not match regex '{kwargs['match']}'"
                    )
                return err

            @staticmethod
            def that(value: Any, **kwargs: Any) -> None:
                if "eq" in kwargs:
                    assert value == kwargs["eq"], (
                        f"Expected {kwargs['eq']}, got {value}"
                    )
                if "ne" in kwargs:
                    assert value != kwargs["ne"], (
                        f"Expected not equal to {kwargs['ne']}, got {value}"
                    )
                if "gt" in kwargs:
                    assert value > kwargs["gt"], (
                        f"Expected > {kwargs['gt']}, got {value}"
                    )
                if "gte" in kwargs:
                    assert value >= kwargs["gte"], (
                        f"Expected >= {kwargs['gte']}, got {value}"
                    )
                if "lt" in kwargs:
                    assert value < kwargs["lt"], (
                        f"Expected < {kwargs['lt']}, got {value}"
                    )
                if "lte" in kwargs:
                    assert value <= kwargs["lte"], (
                        f"Expected <= {kwargs['lte']}, got {value}"
                    )
                if "is_" in kwargs:
                    assert isinstance(value, kwargs["is_"]), (
                        f"Expected instance of {kwargs['is_']}, got {type(value)}"
                    )
                if "none" in kwargs:
                    if kwargs["none"]:
                        assert value is None, f"Expected None, got {value}"
                    else:
                        assert value is not None, "Expected not None, got None"
                if "contains" in kwargs:
                    assert kwargs["contains"] in value, (
                        f"Expected {kwargs['contains']} in {value}"
                    )
                if "length" in kwargs:
                    assert len(value) == kwargs["length"], (
                        f"Expected length {kwargs['length']}, got {len(value)}"
                    )
                if "starts" in kwargs:
                    assert value.startswith(kwargs["starts"]), (
                        f"Expected {value} to start with {kwargs['starts']}"
                    )
                if "ends" in kwargs:
                    assert value.endswith(kwargs["ends"]), (
                        f"Expected {value} to end with {kwargs['ends']}"
                    )
                if "match" in kwargs:
                    assert re.search(kwargs["match"], value), (
                        f"Expected {value} to match regex {kwargs['match']}"
                    )
                if "excludes" in kwargs:
                    assert kwargs["excludes"] not in value, (
                        f"Expected {kwargs['excludes']} to not be in {value}"
                    )
                if "empty" in kwargs:
                    if kwargs["empty"]:
                        assert len(value) == 0, (
                            f"Expected empty, got length {len(value)}"
                        )
                    else:
                        assert len(value) > 0, "Expected non-empty, got length 0"
                if "where" in kwargs:
                    assert kwargs["where"](value), (
                        f"Custom predicate failed for {value}"
                    )

            @staticmethod
            def scope(**kwargs: Any) -> Any:

                class DummyScope:
                    def __enter__(self) -> Self:
                        return self

                    def __exit__(
                        self, exc_type: object, exc_val: object, exc_tb: object
                    ) -> None:
                        pass

                return DummyScope()
