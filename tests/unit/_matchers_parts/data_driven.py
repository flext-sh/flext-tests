"""Private matcher data driven test mixins."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from flext_tests import r, tm
from tests.constants import c
from tests.typings import t


class MatchersDataDrivenMixin:
    """Matcher data driven tests."""

    def test_that_with_paths_data_driven_rules(self) -> None:
        """Validate multiple dotted paths with a single declarative matcher call."""
        payload: t.JsonMapping = {
            "user": {
                "name": "John",
                "age": 33,
                "email": "john@example.com",
            },
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

    def test_that_with_items_data_driven_rules(self) -> None:
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

    def test_that_with_attrs_match_data_driven_rules(self) -> None:
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
            cast("t.JsonValue", user),
            attrs_match={
                "profile.name": {"eq": "Ada"},
                "profile.level": {"gte": 1, "lte": 10},
                "active": {"eq": True},
            },
        )

    def test_ok_with_composed_data_driven_validations(self) -> None:
        """Validate result payload with path extraction plus composed rules."""
        result = r[t.JsonMapping].ok({
            "meta": {"version": "v1", "count": 3},
            "items": ["a", "b", "c"],
        })
        value = tm.ok(
            result,
            paths={
                "meta.version": {"starts": "v"},
                "meta.count": {"eq": 3},
            },
            where=lambda data: isinstance(data, Mapping),
        )
        tm.that(value, is_=dict)
