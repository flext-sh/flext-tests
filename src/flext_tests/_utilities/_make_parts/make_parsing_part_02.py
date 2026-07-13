"""Parsing utilities for flext-tests Make command metadata."""

from __future__ import annotations

from pathlib import Path

from flext_tests import m, p, r, t
from flext_tests._utilities._make_parts.make_parsing_part_01 import (
    FlextTestsMakeParsingUtilitiesMixin as FlextTestsMakeParsingUtilitiesMixinPart01,
)


class FlextTestsMakeParsingUtilitiesMixin(FlextTestsMakeParsingUtilitiesMixinPart01):
    """Parse flext-command TOML headers into typed Make models."""

    @staticmethod
    def make_parse_params(
        value: t.Tests.MakeTomlValue | None,
        path: Path,
    ) -> p.Result[t.SequenceOf[m.Tests.MakeParam]]:
        """Parse command parameter declarations."""
        if value is None:
            return r[t.SequenceOf[m.Tests.MakeParam]].ok(())
        if not isinstance(value, list):
            return r[t.SequenceOf[m.Tests.MakeParam]].fail(
                f"{path}: params deve conter lista",
            )
        params: list[m.Tests.MakeParam] = []
        for item in value:
            if not isinstance(item, dict):
                return r[t.SequenceOf[m.Tests.MakeParam]].fail(
                    f"{path}: params deve conter objetos TOML",
                )
            parsed = t.Tests.MAKE_TOML_TABLE_ADAPTER.validate_python(item)
            param_result = FlextTestsMakeParsingUtilitiesMixin.make_parse_param(
                parsed,
                path,
            )
            if param_result.failure:
                return r[t.SequenceOf[m.Tests.MakeParam]].fail(
                    param_result.error or "param invalid",
                )
            params.append(param_result.value)
        return r[t.SequenceOf[m.Tests.MakeParam]].ok(tuple(params))

    @staticmethod
    def make_parse_mutation_conditions(
        value: t.Tests.MakeTomlValue | None,
        path: Path,
    ) -> p.Result[t.SequenceOf[m.Tests.MakeMutationCondition]]:
        """Parse optional conditional mutation predicates."""
        if value is None:
            return r[t.SequenceOf[m.Tests.MakeMutationCondition]].ok(())
        if not isinstance(value, list):
            return r[t.SequenceOf[m.Tests.MakeMutationCondition]].fail(
                f"{path}: mutates_when deve conter lista",
            )
        conditions: list[m.Tests.MakeMutationCondition] = []
        for item in value:
            if not isinstance(item, dict):
                return r[t.SequenceOf[m.Tests.MakeMutationCondition]].fail(
                    f"{path}: mutates_when deve conter objetos TOML",
                )
            parsed = t.Tests.MAKE_TOML_TABLE_ADAPTER.validate_python(item)
            condition_result = (
                FlextTestsMakeParsingUtilitiesMixin.make_parse_mutation_condition(
                    parsed,
                    path,
                )
            )
            if condition_result.failure:
                return r[t.SequenceOf[m.Tests.MakeMutationCondition]].fail(
                    condition_result.error or "mutation condition invalid",
                )
            conditions.append(condition_result.value)
        return r[t.SequenceOf[m.Tests.MakeMutationCondition]].ok(tuple(conditions))

    @staticmethod
    def make_parse_mutation_condition(
        data: t.Tests.MakeTomlTable,
        path: Path,
    ) -> p.Result[m.Tests.MakeMutationCondition]:
        """Parse one conditional mutation predicate."""
        name_result = FlextTestsMakeParsingUtilitiesMixin.make_require_string(
            data,
            "name",
            path,
        )
        values_result = FlextTestsMakeParsingUtilitiesMixin.make_parse_string_list(
            data,
            "values",
            path,
        )
        if name_result.failure:
            return r[m.Tests.MakeMutationCondition].fail(
                name_result.error or "condition name missing",
            )
        if values_result.failure:
            return r[m.Tests.MakeMutationCondition].fail(
                values_result.error or "condition values invalid",
            )
        if not values_result.value:
            return r[m.Tests.MakeMutationCondition].fail(
                f"{path}: mutates_when.values nao pode estar vazio",
            )
        return r[m.Tests.MakeMutationCondition].ok(
            m.Tests.MakeMutationCondition(
                name=name_result.value,
                values=values_result.value,
            ),
        )

    @staticmethod
    def make_parse_param(
        data: t.Tests.MakeTomlTable,
        path: Path,
    ) -> p.Result[m.Tests.MakeParam]:
        """Parse one command parameter object."""
        name_result = FlextTestsMakeParsingUtilitiesMixin.make_require_string(
            data,
            "name",
            path,
        )
        help_result = FlextTestsMakeParsingUtilitiesMixin.make_require_string(
            data,
            "help",
            path,
        )
        if name_result.failure:
            return r[m.Tests.MakeParam].fail(name_result.error or "param name missing")
        if help_result.failure:
            return r[m.Tests.MakeParam].fail(help_result.error or "param help missing")
        required_raw = data.get("required", False)
        default_raw = data.get("default", "")
        if not isinstance(required_raw, bool):
            return r[m.Tests.MakeParam].fail(
                f"{path}: params.required deve ser booleano",
            )
        if not isinstance(default_raw, str):
            return r[m.Tests.MakeParam].fail(f"{path}: params.default deve ser string")
        choices_result = FlextTestsMakeParsingUtilitiesMixin.make_parse_string_list(
            data,
            "choices",
            path,
        )
        if choices_result.failure:
            return r[m.Tests.MakeParam].fail(choices_result.error or "choices invalid")
        return r[m.Tests.MakeParam].ok(
            m.Tests.MakeParam(
                name=name_result.value,
                help=help_result.value,
                required=required_raw,
                default=default_raw,
                choices=choices_result.value,
            ),
        )

    @staticmethod
    def make_parse_string_map(
        value: t.Tests.MakeTomlValue | None,
        path: Path,
    ) -> p.Result[t.StrPairSequence]:
        """Parse an optional string-to-string mapping."""
        if value is None:
            return r[t.StrPairSequence].ok(())
        if not isinstance(value, dict):
            return r[t.StrPairSequence].fail(f"{path}: target_env deve ser objeto TOML")
        items: list[tuple[str, str]] = []
        for key, item in sorted(value.items()):
            if not key.strip():
                return r[t.StrPairSequence].fail(
                    f"{path}: target_env possui chave invalida",
                )
            if not isinstance(item, str):
                return r[t.StrPairSequence].fail(
                    f"{path}: target_env.{key} deve ser string",
                )
            items.append((key.strip(), item))
        return r[t.StrPairSequence].ok(tuple(items))


__all__: list[str] = ["FlextTestsMakeParsingUtilitiesMixin"]
