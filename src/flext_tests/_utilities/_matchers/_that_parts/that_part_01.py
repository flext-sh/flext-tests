"""Universal matcher parameter and subject helpers."""

from __future__ import annotations

from flext_tests import c, m, p, t
from flext_tests._utilities._matchers._typeguards import (
    FlextTestsMatchersTypeGuardsMixin,
)


class FlextTestsMatchersThatMixin:
    """Universal matcher parameter and subject helpers."""

    class Tests:
        """Container for test utility storages and aliases."""

        class Matchers:
            """Shared helper methods for universal matchers."""

            @staticmethod
            def _that_params(
                kwargs: dict[str, t.Tests.MatcherKwargValue],
            ) -> tuple[
                m.Tests.ThatParams,
                t.Tests.MatcherKwargValue | None,
                t.Tests.MatcherKwargValue | None,
                t.Tests.MatcherKwargValue | None,
                t.Tests.MatcherKwargValue | None,
            ]:
                """Validate matcher kwargs and retain raw non-serializable values."""
                raw_eq = kwargs.get("eq") if "eq" in kwargs else None
                raw_ne = kwargs.get("ne") if "ne" in kwargs else None
                raw_has = kwargs.get("has") if "has" in kwargs else None
                raw_contains = kwargs.get("contains") if "contains" in kwargs else None
                try:
                    params = m.Tests.ThatParams.model_validate(kwargs)
                except c.EXC_BASIC_TYPE:
                    params = (
                        FlextTestsMatchersThatMixin.Tests.Matchers._filtered_params(
                            kwargs
                        )
                    )
                return params, raw_eq, raw_ne, raw_has, raw_contains

            @staticmethod
            def _filtered_params(
                kwargs: dict[str, t.Tests.MatcherKwargValue],
            ) -> m.Tests.ThatParams:
                """Validate kwargs after removing values Pydantic cannot serialize."""
                non_serializable_keys = frozenset({
                    "eq",
                    "ne",
                    "has",
                    "contains",
                    "lacks",
                    "excludes",
                })
                filtered_kwargs = {
                    key: val
                    for key, val in kwargs.items()
                    if key not in non_serializable_keys
                }
                try:
                    return m.Tests.ThatParams.model_validate(filtered_kwargs)
                except c.EXC_BASIC_TYPE as filtered_exc:
                    raise ValueError(
                        f"Parameter validation failed: {filtered_exc}",
                    ) from filtered_exc

            @staticmethod
            def _validate_declared_types(
                value: p.AttributeProbe,
                params: m.Tests.ThatParams,
            ) -> None:
                """Validate ``is_`` and ``not_`` against the original value."""
                value_type_name = type(value).__name__
                if params.is_ is not None:
                    FlextTestsMatchersThatMixin.Tests.Matchers._validate_is_type(
                        value,
                        params,
                        value_type_name,
                    )
                if params.not_ is not None:
                    not_types = (
                        params.not_
                        if isinstance(params.not_, tuple)
                        else (params.not_,)
                    )
                    if any(
                        FlextTestsMatchersTypeGuardsMixin.matches_runtime_type(
                            value,
                            forbidden_type,
                        )
                        for forbidden_type in not_types
                    ):
                        raise AssertionError(
                            params.msg
                            or c.Tests.ERR_TYPE_FAILED.format(
                                expected=f"not {params.not_}",
                                actual=value_type_name,
                            ),
                        )

            @staticmethod
            def _validate_is_type(
                value: p.AttributeProbe,
                params: m.Tests.ThatParams,
                value_type_name: str,
            ) -> None:
                """Validate ``is_`` including FLEXT wrapper/model shortcuts."""
                is_types = (
                    params.is_ if isinstance(params.is_, tuple) else (params.is_,)
                )
                expected_types = tuple(
                    item for item in is_types if isinstance(item, type)
                )
                root_value = getattr(value, "root", None)
                is_mapping_wrapper = (
                    dict in expected_types
                    and isinstance(root_value, dict)
                    and value.__class__.__name__ == "Dict"
                )
                is_model_mapping = (
                    dict in expected_types
                    and isinstance(value, m.BaseModel)
                    and not isinstance(value, m.RootModel)
                )
                is_sequence_wrapper = (
                    list in expected_types
                    and isinstance(root_value, t.SEQUENCE_PAIR_TYPES)
                    and value_type_name == "ObjectList"
                )
                matches_declared_type = any(
                    FlextTestsMatchersTypeGuardsMixin.matches_runtime_type(
                        value,
                        expected_type,
                    )
                    for expected_type in expected_types
                )
                if (
                    matches_declared_type
                    or is_mapping_wrapper
                    or is_model_mapping
                    or is_sequence_wrapper
                ):
                    return
                raise AssertionError(
                    params.msg
                    or f"Assertion failed: {c.Tests.ERR_TYPE_FAILED.format(expected=params.is_, actual=value_type_name)}",
                )

            @staticmethod
            def _is_type_only(
                params: m.Tests.ThatParams,
                raw_eq: t.Tests.MatcherKwargValue | None,
                raw_ne: t.Tests.MatcherKwargValue | None,
            ) -> bool:
                """Return whether only type checks were requested."""
                if params.is_ is None and params.not_ is None:
                    return False
                if raw_eq is not None or raw_ne is not None:
                    return False
                return all(
                    getattr(params, name) is None
                    for name in (
                        "ok",
                        "has",
                        "lacks",
                        "eq",
                        "ne",
                        "gt",
                        "gte",
                        "lt",
                        "lte",
                        "none",
                        "empty",
                        "starts",
                        "ends",
                        "match",
                        "len",
                    )
                )


__all__: list[str] = ["FlextTestsMatchersThatMixin"]
