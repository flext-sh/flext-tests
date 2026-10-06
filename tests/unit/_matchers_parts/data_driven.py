"""Private matcher data driven test mixins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

import pytest

from flext_tests import r, tm
from tests import c, m, t


class TestsFlextTestsMatchersDataDrivenMixin:
    """Matcher data driven tests."""

    @staticmethod
    @pytest.mark.parametrize("value", ["first operand", "different operand"])
    def test_matcher_parameters_resolve_before_public_use(value: str) -> None:
        """Resolve scalar and composed rules on the first public matcher call."""
        tm.that(value, eq=value)
        tm.that({"value": value}, paths={"value": {"eq": value}})
        tm.that([value], items=[{"eq": value}])
        tm.that({"value": value}, attrs_match={"value": {"eq": value}})
        tm.ok(r[str].ok(value), eq=value)
        tm.ok(r[t.JsonMapping].ok({"value": value}), paths={"value": {"eq": value}})
        tm.ok(r[t.StrSequence].ok([value]), items=[{"eq": value}])
        tm.ok(
            r[t.JsonMapping].ok({"value": value}),
            attrs_match={"value": {"eq": value}},
        )
        with pytest.raises(AssertionError):
            tm.that({"value": value}, paths={"value": {"eq": value.upper()}})
        with pytest.raises(AssertionError):
            tm.ok(r[t.StrSequence].ok([value]), items=[{"eq": value.upper()}])

    @staticmethod
    def test_that_with_paths_data_driven_rules() -> None:
        """Validate multiple dotted paths with a single declarative matcher call."""
        payload: t.JsonMapping = {
            "user": {"name": "John", "age": 33, "email": "john@example.com"},
            "status": "active",
        }
        tm.that(
            payload,
            paths={
                "user.name": "John",
                "user.age": {"gte": 18, "lt": 120},
                "user.email": {"match": c.Tests.EMAIL_PATTERN_RE},
                "status": {"eq": "active"},
            },
        )

    @staticmethod
    def test_path_rule_preserves_explicit_none_constraint() -> None:
        payload: t.JsonMapping = {"value": None}

        tm.that(payload, paths={"value": {"eq": None}})
        with pytest.raises(AssertionError):
            tm.that({"value": "present"}, paths={"value": {"eq": None}})

    @staticmethod
    def test_path_rule_accepts_excludes_alias() -> None:
        payload: t.JsonMapping = {"value": "allowed"}

        tm.that(payload, paths={"value": {"excludes": "blocked"}})
        with pytest.raises(AssertionError):
            tm.that({"value": "blocked"}, paths={"value": {"excludes": "blocked"}})

    @staticmethod
    def test_that_with_items_data_driven_rules() -> None:
        """Validate indexed, first/last and all-item rules declaratively."""
        rows: t.StrSequence = ["alpha", "beta", "gamma"]
        tm.that(
            rows,
            items={
                "first": {"starts": "al"},
                1: {"eq": "beta"},
                "last": {"ends": "ma"},
                "all": {"is_": str},
            },
        )

    @staticmethod
    def test_item_rules_reject_string_rule_container() -> None:
        with pytest.raises(m.ValidationError, match=r"for ThatParams\nitems") as error:
            tm.that(["alpha"], items="alpha")
        tm.that({item["loc"][0] for item in error.value.errors()}, eq={"items"})

    @staticmethod
    def test_that_with_attrs_match_data_driven_rules() -> None:
        """Validate nested attributes using one declarative attrs_match spec."""

        class Profile:
            def __init__(self) -> None:
                self.name = "Ada"
                self.level = 7

        class User:
            def __init__(self) -> None:
                self.profile = Profile()
                self.active = True

        user = User()
        tm.that(
            user,
            attrs_match={
                "profile.name": {"eq": "Ada"},
                "profile.level": {"gte": 1, "lte": 10},
                "active": {"eq": True},
            },
        )

    @staticmethod
    def test_ok_with_composed_data_driven_validations() -> None:
        """Validate result payload with path extraction plus composed rules."""

        def is_mapping(data: t.Tests.NativeMatchValue) -> bool:
            return isinstance(data, Mapping)

        result = r[t.JsonMapping].ok({
            "meta": {"version": "v1", "count": 3},
            "items": ["a", "b", "c"],
        })
        value = tm.ok(
            result,
            paths={"meta.version": {"starts": "v"}, "meta.count": {"eq": 3}},
            where=is_mapping,
        )
        tm.that(value, is_=dict)
