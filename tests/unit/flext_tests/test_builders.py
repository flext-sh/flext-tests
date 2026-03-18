"""Unit tests for flext_tests.builders module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

import pytest
from flext_core import r
from pydantic import BaseModel, ValidationError

from flext_tests import tm
from tests import c, t, tb
from tests.test_utils import assertion_helpers


def _as_builder_dict(value: t.Tests.object) -> t.Tests.Builders.BuilderDict:
    tm.that(isinstance(value, Mapping), eq=True)
    typed_mapping = cast("Mapping[str, t.Tests.object]", value)
    return cast("t.Tests.Builders.BuilderDict", dict(typed_mapping.items()))


def _as_builder_result(
    value: t.Tests.Builders.BuilderValue | r[t.Tests.Builders.BuilderValue],
) -> r[t.Tests.Builders.BuilderDict]:
    tm.that(isinstance(value, r), eq=True)
    return cast("r[t.Tests.Builders.BuilderDict]", value)


def _as_parametrized_cases(
    value: t.Tests.object,
) -> list[t.Tests.Builders.ParametrizedCase]:
    tm.that(isinstance(value, list), eq=True)
    return cast("list[t.Tests.Builders.ParametrizedCase]", value)


class TestFlextTestsBuilders:
    """Test suite for tb class."""

    def test_init(self) -> None:
        """Test tb initialization."""
        builder = tb()
        tm.that(builder is not None, eq=True)
        data = _as_builder_dict(builder.build())
        tm.that(isinstance(data, dict), eq=True)
        tm.that(data == {}, eq=True)

    def test_with_users_default(self) -> None:
        """Test with_users with default count."""
        builder = tb()
        result = builder.with_users()
        tm.that(result is builder, eq=True)
        data = _as_builder_dict(builder.build())
        tm.that("users" in data, eq=True)
        users = cast("list[dict[str, str | bool]]", data["users"])
        tm.that(len(users) == 5, eq=True)
        first_user = users[0]
        tm.that("id" in first_user, eq=True)
        tm.that("name" in first_user, eq=True)
        tm.that("email" in first_user, eq=True)
        tm.that("active" in first_user, eq=True)
        tm.that(first_user["name"] == "User 0", eq=True)

    def test_with_users_custom_count(self) -> None:
        """Test with_users with custom count."""
        builder = tb()
        builder.with_users(count=3)
        data = _as_builder_dict(builder.build())
        users = cast("list[dict[str, str | bool]]", data["users"])
        tm.that(len(users) == 3, eq=True)

    def test_with_configs_development(self) -> None:
        """Test with_configs in development mode."""
        builder = tb()
        result = builder.with_configs(production=False)
        tm.that(result is builder, eq=True)
        data = _as_builder_dict(builder.build())
        tm.that("configs" in data, eq=True)
        config = cast("dict[str, str | int | bool]", data["configs"])
        tm.that(config["environment"] == "development", eq=True)
        tm.that(config["debug"] is True, eq=True)
        tm.that(config["service_type"] == "api", eq=True)
        tm.that(config["timeout"] == 30, eq=True)

    def test_with_configs_production(self) -> None:
        """Test with_configs in production mode."""
        builder = tb()
        builder.with_configs(production=True)
        data = _as_builder_dict(builder.build())
        config = cast("dict[str, str | int | bool]", data["configs"])
        tm.that(config["environment"] == "production", eq=True)
        tm.that(config["debug"] is False, eq=True)

    def test_with_validation_fields_default(self) -> None:
        """Test with_validation_fields with default count."""
        builder = tb()
        result = builder.with_validation_fields()
        tm.that(result is builder, eq=True)
        data = _as_builder_dict(builder.build())
        tm.that("validation_fields" in data, eq=True)
        fields = cast("dict[str, t.Tests.object]", data["validation_fields"])
        valid_emails = cast("list[str]", fields["valid_emails"])
        tm.that(len(valid_emails) == 5, eq=True)
        tm.that(valid_emails[0] == "user0@example.com", eq=True)
        invalid_emails = cast("list[str]", fields["invalid_emails"])
        tm.that(len(invalid_emails) == 3, eq=True)
        tm.that(
            fields["valid_hostnames"] == ["example.com", c.Network.LOCALHOST], eq=True
        )

    def test_with_validation_fields_custom_count(self) -> None:
        """Test with_validation_fields with custom count."""
        builder = tb()
        builder.with_validation_fields(count=3)
        data = _as_builder_dict(builder.build())
        validation_fields = cast(
            "dict[str, t.Tests.object]",
            data["validation_fields"],
        )
        valid_emails = cast("list[str]", validation_fields["valid_emails"])
        tm.that(len(valid_emails) == 3, eq=True)

    def test_build_empty(self) -> None:
        """Test build with no data added."""
        builder = tb()
        data = _as_builder_dict(builder.build())
        tm.that(isinstance(data, dict), eq=True)
        tm.that(data == {}, eq=True)

    def test_build_full_dataset(self) -> None:
        """Test build with all data types added."""
        builder = tb()
        builder.with_users(2).with_configs(production=True).with_validation_fields(2)
        data = _as_builder_dict(builder.build())
        tm.that("users" in data, eq=True)
        tm.that("configs" in data, eq=True)
        tm.that("validation_fields" in data, eq=True)
        users = cast("list[dict[str, str | bool]]", data["users"])
        configs = cast("dict[str, str | int | bool]", data["configs"])
        tm.that(len(users) == 2, eq=True)
        tm.that(configs["environment"] == "production", eq=True)

    def test_reset(self) -> None:
        """Test reset clears builder state."""
        builder = tb()
        builder.with_users(3).with_configs()
        data_before = _as_builder_dict(builder.build())
        tm.that("users" in data_before, eq=True)
        tm.that("configs" in data_before, eq=True)
        result = builder.reset()
        tm.that(result is builder, eq=True)
        data_after = _as_builder_dict(builder.build())
        tm.that(data_after == {}, eq=True)

    def test_method_chaining(self) -> None:
        """Test fluent interface method chaining."""
        builder = tb()
        result = (
            builder
            .with_users(2)
            .with_configs(production=False)
            .with_validation_fields(3)
            .build()
        )
        tm.that(isinstance(result, dict), eq=True)
        tm.that("users" in result, eq=True)
        tm.that("configs" in result, eq=True)
        tm.that("validation_fields" in result, eq=True)

    def test_multiple_calls_overwrite(self) -> None:
        """Test multiple calls to same method overwrite previous data."""
        builder = tb()
        builder.with_users(2)
        data1 = _as_builder_dict(builder.build())
        users1 = cast("list[dict[str, str | bool]]", data1["users"])
        tm.that(len(users1) == 2, eq=True)
        builder.with_users(5)
        data2 = _as_builder_dict(builder.build())
        users2 = cast("list[dict[str, str | bool]]", data2["users"])
        tm.that(len(users2) == 5, eq=True)

    def test_add_direct_value(self) -> None:
        """Test add() with direct value."""
        builder = tb()
        builder.add("name", "test")
        data = _as_builder_dict(builder.build())
        tm.that(data["name"] == "test", eq=True)

    def test_add_with_result_ok(self) -> None:
        """Test add() with result_ok parameter."""
        builder = tb()
        builder.add("result", result_ok=42)
        data = _as_builder_dict(builder.build())
        result = cast("r[int]", cast("object", data["result"]))
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == 42, eq=True)

    def test_add_with_result_fail(self) -> None:
        """Test add() with result_fail parameter."""
        builder = tb()
        builder.add("error", result_fail="Failed", result_code="E001")
        data = _as_builder_dict(builder.build())
        result = cast("r[str]", cast("object", data["error"]))
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("Failed" in str(result.error), eq=True)

    def test_add_with_items_and_map(self) -> None:
        """Test add() with items and items_map."""

        def _double_item(item: t.Tests.object) -> t.Tests.object:
            tm.that(isinstance(item, int), eq=True)
            if not isinstance(item, int):
                raise TypeError(f"Expected int, got {type(item)}")
            return item * 2

        builder = tb()
        builder.add(
            "doubled",
            items=[1, 2, 3],
            items_map=cast("t.Tests.object", _double_item),
        )
        data = _as_builder_dict(builder.build())
        doubled = cast("list[int]", data["doubled"])
        tm.that(doubled == [2, 4, 6], eq=True)

    def test_add_with_entries_and_filter(self) -> None:
        """Test add() with entries and entries_filter."""
        builder = tb()
        builder.add(
            "filtered",
            entries={"a": 1, "b": 2, "c": 3},
            entries_filter=cast("t.Tests.object", cast("object", {"a", "c"})),
        )
        data = _as_builder_dict(builder.build())
        filtered = cast("dict[str, int]", data["filtered"])
        tm.that("a" in filtered, eq=True)
        tm.that("c" in filtered, eq=True)
        tm.that("b" not in filtered, eq=True)

    def test_add_with_factory(self) -> None:
        """Test add() with factory parameter."""
        builder = tb()
        builder.add("users", factory="users", count=3)
        data = _as_builder_dict(builder.build())
        users = cast("list[dict[str, t.Tests.object]]", data["users"])
        tm.that(len(users) == 3, eq=True)

    def test_add_with_mapping(self) -> None:
        """Test add() with mapping parameter."""
        builder = tb()
        builder.add("config", mapping={"env": "test", "debug": True})
        data = _as_builder_dict(builder.build())
        config = cast("dict[str, t.Tests.object]", data["config"])
        tm.that(config["env"] == "test", eq=True)
        tm.that(config["debug"] is True, eq=True)

    def test_add_with_sequence(self) -> None:
        """Test add() with sequence parameter."""
        builder = tb()
        builder.add("items", sequence=[1, 2, 3])
        data = _as_builder_dict(builder.build())
        items = cast("list[int]", data["items"])
        tm.that(items == [1, 2, 3], eq=True)

    def test_add_with_merge(self) -> None:
        """Test add() with merge parameter."""
        builder = tb()
        builder.add("config", mapping={"a": 1, "b": 2})
        builder.add("config", mapping={"b": 3, "c": 4}, merge=True)
        data = _as_builder_dict(builder.build())
        config = cast("dict[str, int]", data["config"])
        tm.that("a" in config or "b" in config or "c" in config, eq=True)

    def test_build_as_list(self) -> None:
        """Test build() with as_list parameter."""
        builder = tb()
        builder.add("a", 1).add("b", 2)
        result = builder.build(as_list=True)
        items = cast("list[tuple[str, object]]", result)
        tm.that(len(items) == 2, eq=True)
        tm.that(("a", 1) in items, eq=True)
        tm.that(("b", 2) in items, eq=True)

    def test_build_keys_only(self) -> None:
        """Test build() with keys_only parameter."""
        builder = tb()
        builder.add("a", 1).add("b", 2)
        keys = builder.build(keys_only=True)
        tm.that(isinstance(keys, list), eq=True)
        tm.that("a" in keys, eq=True)
        tm.that("b" in keys, eq=True)

    def test_build_values_only(self) -> None:
        """Test build() with values_only parameter."""
        builder = tb()
        builder.add("a", 1).add("b", 2)
        values = builder.build(values_only=True)
        tm.that(isinstance(values, list), eq=True)
        tm.that(1 in values, eq=True)
        tm.that(2 in values, eq=True)

    def test_build_with_flatten(self) -> None:
        """Test build() with flatten parameter."""
        builder = tb()
        builder.set("a.b.c", 42)
        flattened_raw = builder.build(flatten=True)
        flattened = cast("dict[str, t.Tests.object]", flattened_raw)
        tm.that(isinstance(flattened, dict), eq=True)
        tm.that("a.b.c" in flattened, eq=True)
        tm.that(flattened["a.b.c"] == 42, eq=True)

    def test_build_with_filter_none(self) -> None:
        """Test build() with filter_none parameter."""
        builder = tb()
        builder.add("a", 1).add("b", None).add("c", 3)
        filtered_raw = builder.build(filter_none=True)
        filtered = cast("dict[str, t.Tests.object]", filtered_raw)
        tm.that("a" in filtered, eq=True)
        tm.that("b" not in filtered, eq=True)
        tm.that("c" in filtered, eq=True)

    def test_build_as_parametrized(self) -> None:
        """Test build() with as_parametrized parameter."""
        builder = tb()
        builder.add("test_id", "case_1").add("value", 42)
        cases_raw = builder.build(as_parametrized=True)
        cases = _as_parametrized_cases(cases_raw)
        tm.that(isinstance(cases, list), eq=True)
        tm.that(len(cases) == 1, eq=True)
        test_id, data = cases[0]
        tm.that(test_id == "case_1", eq=True)
        tm.that(data["value"] == 42, eq=True)

    def test_build_with_validate_with(self) -> None:
        """Test build() with validate_with parameter."""

        def _has_expected_count(
            data: t.Tests.Builders.BuilderOutputDict,
        ) -> bool:
            return data["count"] == 5

        builder = tb()
        builder.add("count", 5)
        build_result = builder.build(
            validate_with=cast(
                "t.Tests.object",
                _has_expected_count,
            ),
        )
        if isinstance(build_result, dict):
            data = build_result
        elif isinstance(build_result, BaseModel):
            data = build_result.model_dump()
        else:
            msg = f"Expected dict, got {type(build_result)}"
            raise AssertionError(msg)
        tm.that(data["count"] == 5, eq=True)

    def test_build_with_map_result(self) -> None:
        """Test build() with map_result parameter."""

        def _double_x(
            data: t.Tests.Builders.BuilderOutputDict,
        ) -> t.Tests.object:
            tm.that(isinstance(data["x"], int), eq=True)
            x_val = data["x"]
            if not isinstance(x_val, int):
                raise TypeError(f"Expected int, got {type(x_val)}")
            return x_val * 2

        builder = tb()
        builder.add("x", 1)
        build_result = builder.build(
            map_result=cast(
                "t.Tests.object",
                _double_x,
            ),
        )
        doubled = cast("int", build_result)
        tm.that(doubled == 2, eq=True)

    def test_to_result_success(self) -> None:
        """Test to_result() with success case."""
        builder = tb()
        builder.add("x", 1)
        result_raw = builder.to_result()
        result = _as_builder_result(result_raw)
        _ = assertion_helpers.assert_flext_result_success(result)
        data = result.value
        tm.that(data["x"] == 1, eq=True)

    def test_to_result_with_error(self) -> None:
        """Test to_result() with error parameter."""
        builder = tb()
        result = _as_builder_result(
            builder.to_result(error="Failed", error_code="E001"),
        )
        _ = assertion_helpers.assert_flext_result_failure(result)
        tm.that("Failed" in str(result.error), eq=True)

    def test_to_result_with_unwrap(self) -> None:
        """Test to_result() with unwrap parameter."""
        builder = tb()
        builder.add("x", 1)
        result_raw = builder.to_result(unwrap=True)
        data = cast("t.Tests.Builders.BuilderDict", result_raw)
        tm.that(isinstance(data, dict), eq=True)
        tm.that(data["x"] == 1, eq=True)

    def test_to_result_with_validate(self) -> None:
        """Test to_result() with validate parameter."""

        def _has_count(data: t.Tests.Builders.BuilderDict) -> bool:
            return data["count"] == 5

        builder = tb()
        builder.add("count", 5)
        result_raw = builder.to_result(
            validate=cast(
                "t.Tests.object",
                _has_count,
            ),
        )
        result = _as_builder_result(result_raw)
        _ = assertion_helpers.assert_flext_result_success(result)

    def test_copy_builder(self) -> None:
        """Test copy_builder() creates independent copy."""
        builder = tb()
        builder.add("base", 1)
        copied = builder.copy_builder()
        copied.add("extra", 2)
        tm.that(builder.build() == {"base": 1}, eq=True)
        tm.that(copied.build() == {"base": 1, "extra": 2}, eq=True)

    def test_fork(self) -> None:
        """Test fork() creates copy with updates."""
        builder = tb()
        builder.add("base", 1)
        forked = builder.fork(extra=2, another=3)
        tm.that(builder.build() == {"base": 1}, eq=True)
        forked_data = _as_builder_dict(forked.build())
        tm.that(forked_data["base"] == 1, eq=True)
        tm.that(forked_data["extra"] == 2, eq=True)
        tm.that(forked_data["another"] == 3, eq=True)

    def test_merge_from(self) -> None:
        """Test merge_from() merges data from another builder."""
        builder1 = tb()
        builder1.add("a", 1)
        builder2 = tb()
        builder2.add("b", 2)
        builder1.merge_from(builder2)
        data = _as_builder_dict(builder1.build())
        tm.that(data["a"] == 1, eq=True)
        tm.that(data["b"] == 2, eq=True)

    def test_batch(self) -> None:
        """Test batch() creates batch of scenarios."""
        builder = tb()
        builder.batch(
            "cases",
            [("valid", "test@example.com"), ("invalid", "not-email")],
        )
        data = _as_builder_dict(builder.build())
        cases = cast("list[t.Tests.Builders.ParametrizedCase]", data["cases"])
        tm.that(len(cases) == 2, eq=True)

    def test_batch_with_results(self) -> None:
        """Test batch() with as_results parameter."""
        builder = tb()
        builder.batch("results", [("success", 42), ("another", 100)], as_results=True)
        data = _as_builder_dict(builder.build())
        results = cast("list[r[int]]", data["results"])
        tm.that(len(results) == 2, eq=True)
        tm.that(all(r.is_success for r in results), eq=True)

    def test_scenarios(self) -> None:
        """Test scenarios() creates parametrized test cases."""
        builder = tb()
        cases = builder.scenarios(
            ("test_valid", {"input": "hello", "expected": 5}),
            ("test_empty", {"input": "", "expected": 0}),
        )
        tm.that(len(cases) == 2, eq=True)
        tm.that(cases[0][0] == "test_valid", eq=True)
        tm.that(cases[0][1]["input"] == "hello", eq=True)

    def test_tests_result_ok(self) -> None:
        """Test tb.Tests.Result.ok()."""
        result = tb.Tests.Result.ok(42)
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == 42, eq=True)

    def test_tests_result_fail(self) -> None:
        """Test tb.Tests.Result.fail()."""
        result_raw: r[str] = tb.Tests.Result.fail("Error", code="E001")
        result = result_raw
        _ = assertion_helpers.assert_flext_result_failure(result)

    def test_tests_result_batch_ok(self) -> None:
        """Test tb.Tests.Result.batch_ok()."""
        results = tb.Tests.Result.batch_ok([1, 2, 3])
        tm.that(len(results) == 3, eq=True)
        tm.that(all(r.is_success for r in results), eq=True)

    def test_tests_result_all_success(self) -> None:
        """Test tb.Tests.Result.all_success()."""
        results = [r[int].ok(1), r[int].ok(2), r[int].ok(3)]
        tm.that(tb.Tests.Result.all_success(results) is True, eq=True)

    def test_tests_data_merged(self) -> None:
        """Test tb.Tests.Data.merged()."""
        merged = tb.Tests.Data.merged({"a": 1}, {"b": 2}, {"c": 3})
        tm.that(merged["a"] == 1, eq=True)
        tm.that(merged["b"] == 2, eq=True)
        tm.that(merged["c"] == 3, eq=True)

    def test_tests_data_flatten(self) -> None:
        """Test tb.Tests.Data.flatten()."""
        nested = {"a": {"b": {"c": 42}}}
        flattened = tb.Tests.Data.flatten(nested)
        tm.that("a.b.c" in flattened, eq=True)
        tm.that(flattened["a.b.c"] == 42, eq=True)

    def test_tests_data_transform(self) -> None:
        """Test tb.Tests.Data.transform()."""
        doubled = tb.Tests.Data.transform([1, 2, 3], lambda x: x * 2)
        tm.that(doubled == [2, 4, 6], eq=True)

    def test_tests_model_user(self) -> None:
        """Test tb.Tests.Model.user()."""
        user = tb.Tests.Model.user(name="Test", email="test@example.com")
        tm.that(user.name == "Test", eq=True)
        tm.that(user.email == "test@example.com", eq=True)

    def test_tests_batch_scenarios(self) -> None:
        """Test tb.Tests.Batch.scenarios()."""
        cases = tb.Tests.Batch.scenarios(("case1", 1), ("case2", 2))
        tm.that(len(cases) == 2, eq=True)
        tm.that(cases[0] == ("case1", 1), eq=True)

    def test_add_params_validation_count_positive(self) -> None:
        """Test AddParams validates count is positive."""
        builder = tb()
        with pytest.raises((ValueError, ValidationError)):
            builder.add("items", factory="users", count=0)

    def test_build_params_validation_parametrize_key_not_empty(self) -> None:
        """Test BuildParams validates parametrize_key is not empty."""
        builder = tb()
        builder.add("test_id", "case_1")
        with pytest.raises((ValueError, ValidationError)):
            builder.build(as_parametrized=True, parametrize_key="")

    def test_to_result_params_validation_error_code_with_error(self) -> None:
        """Test ToResultParams validates error_code is only with error."""
        builder = tb()
        result_raw = builder.to_result(error_code="E001")
        result = _as_builder_result(result_raw)
        _ = assertion_helpers.assert_flext_result_success(result)

    def test_batch_params_validation_scenarios_not_empty(self) -> None:
        """Test BatchParams validates scenarios is not empty."""
        builder = tb()
        with pytest.raises((ValueError, ValidationError)):
            builder.batch("cases", [])

    def test_merge_from_params_validation_strategy(self) -> None:
        """Test MergeFromParams validates strategy is valid."""
        builder1 = tb()
        builder1.add("a", 1)
        builder2 = tb()
        builder2.add("b", 2)
        with pytest.raises((ValueError, ValidationError)):
            builder1.merge_from(builder2, strategy="invalid")

    def test_add_uses_model_from_kwargs(self) -> None:
        """Test add() uses u.from_kwargs() for validation."""
        builder = tb()
        builder.add("value", value=42, count=1)
        data = _as_builder_dict(builder.build())
        tm.that(data["value"] == 42, eq=True)

    def test_build_uses_model_from_kwargs(self) -> None:
        """Test build() uses u.from_kwargs() for validation."""
        builder = tb()
        builder.add("x", 1)
        data_raw = builder.build(filter_none=True)
        data = cast("t.Tests.Builders.BuilderDict", data_raw)
        tm.that(data["x"] == 1, eq=True)

    def test_to_result_uses_model_from_kwargs(self) -> None:
        """Test to_result() uses u.from_kwargs() for validation."""
        builder = tb()
        builder.add("x", 1)
        result_raw = builder.to_result(unwrap=False)
        result = _as_builder_result(result_raw)
        _ = assertion_helpers.assert_flext_result_success(result)

    def test_merge_from_uses_merge_utility(self) -> None:
        """Test merge_from() uses u.merge() utility."""
        builder1 = tb()
        builder1.add("a", 1)
        builder2 = tb()
        builder2.add("b", 2)
        builder1.merge_from(builder2, strategy="deep")
        data = _as_builder_dict(builder1.build())
        tm.that("a" in data, eq=True)
        tm.that("b" in data, eq=True)

    def test_data_merged_uses_merge_utility(self) -> None:
        """Test tb.Tests.Data.merged() uses u.merge()."""
        merged = tb.Tests.Data.merged({"a": 1}, {"b": 2})
        tm.that(merged["a"] == 1, eq=True)
        tm.that(merged["b"] == 2, eq=True)

    def test_data_transform_uses_collection_map(self) -> None:
        """Test tb.Tests.Data.transform() uses u.map()."""
        doubled = tb.Tests.Data.transform([1, 2, 3], lambda x: x * 2)
        tm.that(doubled == [2, 4, 6], eq=True)

    def test_result_ok_delegates_to_tt_res(self) -> None:
        """Test tb.Tests.Result.ok() delegates to tt.res()."""
        result = tb.Tests.Result.ok(42)
        _ = assertion_helpers.assert_flext_result_success(result)
        tm.that(result.value == 42, eq=True)

    def test_result_fail_delegates_to_tt_res(self) -> None:
        """Test tb.Tests.Result.fail() delegates to tt.res()."""
        result_raw: r[str] = tb.Tests.Result.fail("Error")
        result = result_raw
        _ = assertion_helpers.assert_flext_result_failure(result)

    def test_result_batch_ok_delegates_to_tt_results(self) -> None:
        """Test tb.Tests.Result.batch_ok() delegates to tt.results()."""
        results = tb.Tests.Result.batch_ok([1, 2, 3])
        tm.that(len(results) == 3, eq=True)
        tm.that(all(r.is_success for r in results), eq=True)

    def test_model_user_delegates_to_tt_model(self) -> None:
        """Test tb.Tests.Model.user() delegates to tt.model()."""
        user = tb.Tests.Model.user(name="Test", email="test@example.com")
        tm.that(user.name == "Test", eq=True)
        tm.that(user.email == "test@example.com", eq=True)

    def test_model_config_delegates_to_tt_model(self) -> None:
        """Test tb.Tests.Model.config() delegates to tt.model()."""
        config = tb.Tests.Model.config(service_type="api", debug=True)
        tm.that(config.service_type == "api", eq=True)
        tm.that(config.debug is True, eq=True)

    def test_model_batch_users_delegates_to_tt_batch(self) -> None:
        """Test tb.Tests.Model.batch_users() delegates to tt.batch()."""
        users = tb.Tests.Model.batch_users(count=3)
        tm.that(len(users) == 3, eq=True)

    def test_result_assert_success_delegates_to_tu(self) -> None:
        """Test tb.Tests.Result.assert_success() delegates to tu.Tests.Result."""
        result = r[int].ok(42)
        value = tb.Tests.Result.assert_success(result)
        tm.that(value == 42, eq=True)

    def test_result_assert_failure_delegates_to_tu(self) -> None:
        """Test tb.Tests.Result.assert_failure() delegates to tu.Tests.Result."""
        result: r[t.Tests.object] = r[t.Tests.object].fail("Error")
        error: str = tb.Tests.Result.assert_failure(result)
        tm.that("Error" in error, eq=True)

    def test_batch_parametrized_delegates_to_tu(self) -> None:
        """Test tb.Tests.Batch.parametrized() delegates to tu.Tests.GenericHelpers."""
        cases = tb.Tests.Batch.parametrized(
            success_values=[1, 2, 3],
            failure_errors=["error1", "error2"],
        )
        tm.that(len(cases) > 0, eq=True)
        tm.that(all(isinstance(c, tuple) and len(c) == 2 for c in cases), eq=True)

    def test_batch_test_cases_delegates_to_tu(self) -> None:
        """Test tb.Tests.Batch.test_cases() delegates to tu.Tests.TestCaseHelpers."""
        cases = tb.Tests.Batch.test_cases(
            operation="add",
            descriptions=["test1", "test2"],
            inputs=[{"a": 1, "b": 2}, {"a": 3, "b": 4}],
            expected=[3, 7],
        )
        tm.that(len(cases) == 2, eq=True)

    def test_data_id_delegates_to_tu_factory(self) -> None:
        """Test tb.Tests.Data.id() delegates to tu.Tests.Factory.generate_id()."""
        test_id = tb.Tests.Data.id()
        tm.that(isinstance(test_id, str), eq=True)
        tm.that(len(test_id) > 0, eq=True)

    def test_data_short_id_delegates_to_tu_factory(self) -> None:
        """Test tb.Tests.Data.short_id() delegates to tu.Tests.Factory.generate_short_id()."""
        short_id = tb.Tests.Data.short_id(length=8)
        tm.that(isinstance(short_id, str), eq=True)
        tm.that(len(short_id) == 8, eq=True)

    def test_operation_simple_delegates_to_tu_factory(self) -> None:
        """Test tb.Tests.Operation.simple() delegates to tu.Tests.Factory."""
        op = tb.Tests.Operation.simple()
        result = op()
        tm.that(isinstance(result, str), eq=True)

    def test_operation_add_delegates_to_tu_factory(self) -> None:
        """Test tb.Tests.Operation.add() delegates to tu.Tests.Factory."""
        op = tb.Tests.Operation.add()
        result = op(2, 3)
        tm.that(result == 5, eq=True)

    def test_operation_execute_service_delegates_to_tu_factory(self) -> None:
        """Test tb.Tests.Operation.execute_service() delegates to tu.Tests.Factory."""
        result = tb.Tests.Operation.execute_service()
        _ = assertion_helpers.assert_flext_result_success(result)
