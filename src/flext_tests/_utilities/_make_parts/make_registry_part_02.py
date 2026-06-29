"""Registry command model builder for flext-tests Make commands."""

from __future__ import annotations

from pathlib import Path

from flext_tests import m, p, r, t
from flext_tests._utilities._make_parts.make_registry_part_01 import (
    FlextTestsMakeRegistryUtilitiesMixin as FlextTestsMakeRegistryUtilitiesMixinPart01,
)
from flext_tests._utilities.make_contract import FlextTestsMakeContractUtilitiesMixin
from flext_tests._utilities.make_parsing import FlextTestsMakeParsingUtilitiesMixin


class FlextTestsMakeRegistryUtilitiesMixin(FlextTestsMakeRegistryUtilitiesMixinPart01):
    """Build registry command models from validated metadata."""

    @staticmethod
    def _make_command_from_data(
        path: Path,
        data: t.Tests.MakeTomlTable,
        verb: str,
        what: str,
    ) -> p.Result[m.Tests.MakeCommand]:
        """Build a command model from validated TOML header data."""
        values: t.MutableStrMapping = {}
        for field in ("domain", "summary", "description", "example"):
            value_result = FlextTestsMakeParsingUtilitiesMixin.make_require_string(
                data,
                field,
                path,
            )
            if value_result.failure:
                return r[m.Tests.MakeCommand].fail(
                    value_result.error or f"{field} missing"
                )
            values[field] = value_result.value

        mutates_result = FlextTestsMakeParsingUtilitiesMixin.make_require_bool(
            data,
            "mutates",
            path,
        )
        mutates_when_result = (
            FlextTestsMakeParsingUtilitiesMixin.make_parse_mutation_conditions(
                data.get("mutates_when"),
                path,
            )
        )
        aliases_result = FlextTestsMakeParsingUtilitiesMixin.make_parse_aliases(
            data.get("aliases"),
            path,
        )
        params_result = FlextTestsMakeParsingUtilitiesMixin.make_parse_params(
            data.get("params"),
            path,
        )
        rules_result = FlextTestsMakeParsingUtilitiesMixin.make_parse_string_list(
            data,
            "rules",
            path,
        )
        target_result = (
            FlextTestsMakeParsingUtilitiesMixin.make_require_optional_string(
                data,
                "target",
                path,
            )
        )
        target_env_result = FlextTestsMakeParsingUtilitiesMixin.make_parse_string_map(
            data.get("target_env"),
            path,
        )
        for result in (
            mutates_result,
            mutates_when_result,
            aliases_result,
            params_result,
            rules_result,
            target_result,
            target_env_result,
        ):
            if result.failure:
                return r[m.Tests.MakeCommand].fail(
                    result.error or "command metadata invalid"
                )

        command = m.Tests.MakeCommand(
            verb=verb,
            what=what,
            domain=values["domain"],
            summary=values["summary"],
            description=values["description"],
            example=values["example"],
            path=path,
            mutates=mutates_result.value,
            mutates_when=mutates_when_result.value,
            aliases=aliases_result.value,
            params=params_result.value,
            rules=rules_result.value,
            target=target_result.value,
            target_env=target_env_result.value,
        )
        contract_result = (
            FlextTestsMakeContractUtilitiesMixin.make_validate_command_contract(command)
        )
        if contract_result.failure:
            return r[m.Tests.MakeCommand].fail(
                contract_result.error or "command contract invalid"
            )
        return r[m.Tests.MakeCommand].ok(command)


__all__: list[str] = ["FlextTestsMakeRegistryUtilitiesMixin"]
