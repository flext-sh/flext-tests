"""Contract utilities for flext-tests Make commands."""

from __future__ import annotations

from flext_tests import c, m, p, r, t
from flext_tests._utilities.make_parsing import FlextTestsMakeParsingUtilitiesMixin


class FlextTestsMakeContractUtilitiesMixin(FlextTestsMakeParsingUtilitiesMixin):
    """Validate Make command contracts."""

    @staticmethod
    def make_param_value(
        param: m.Tests.MakeParam,
        command: m.Tests.MakeCommand,
        env: t.MappingKV[str, str],
    ) -> str:
        """Return the current environment-backed value for one parameter."""
        if param.name == c.Tests.MAKE_WHAT_PARAM:
            what: str = command.what
            return what
        name: str = param.name
        default: str = param.default
        value: str = env.get(name, default)
        return value.strip()

    @staticmethod
    def make_validate_invocation(
        command: m.Tests.MakeCommand,
        env: t.MappingKV[str, str],
        *,
        require_required: bool = True,
    ) -> p.Result[bool]:
        """Validate parameter values for one command invocation."""
        for param in command.params:
            value = FlextTestsMakeContractUtilitiesMixin.make_param_value(
                param,
                command,
                env,
            )
            if require_required and param.required and not value:
                return r[bool].fail(
                    f"{command.verb} WHAT={command.what}: parametro obrigatorio "
                    f"ausente: {param.name}; exemplo: {command.example}",
                )
            if value and param.choices and value not in param.choices:
                valid = "|".join(param.choices)
                return r[bool].fail(
                    f"{command.verb} WHAT={command.what}: {param.name}={value!r} "
                    f"invalido; validos: {valid}",
                )
        return r[bool].ok(True)

    @staticmethod
    def make_validate_command_contract(
        command: m.Tests.MakeCommand,
    ) -> p.Result[bool]:
        """Validate one command against the generic dispatcher contract."""
        param_by_name = {param.name: param for param in command.params}
        if command.mutates:
            for name in c.Tests.MAKE_MUTATION_REQUIRED_PARAMS:
                param = param_by_name.get(name)
                if param is None or not param.required:
                    return r[bool].fail(
                        f"{command.path}: parametro {name} deve ser obrigatorio",
                    )
            apply_param = param_by_name.get(c.Tests.MAKE_APPLY_PARAM)
            if (
                apply_param
                and c.Tests.MAKE_DISPATCH_ENV_VALUE not in apply_param.choices
            ):
                return r[bool].fail(
                    f"{command.path}: APPLY deve declarar choices contendo Y",
                )
        if command.path.suffix not in c.Tests.MAKE_COMMAND_SUFFIXES:
            return r[bool].fail(
                f"{command.path}: comando deve usar extensao .py ou .sh",
            )
        if command.path.name != f"{command.what}.py" and command.path.suffix != ".sh":
            return r[bool].fail(
                f"{command.path}: comando deve usar extensao .py ou .sh",
            )
        if not command.summary.strip():
            return r[bool].fail(f"{command.path}: campo summary nao pode estar vazio")
        if command.target and command.path.suffix != ".py":
            return r[bool].fail(
                f"{command.path}: target header-only deve usar arquivo .py",
            )
        if command.target_env and not command.target:
            return r[bool].fail(f"{command.path}: target_env exige target")
        if command.target:
            body_result = FlextTestsMakeParsingUtilitiesMixin.make_has_executable_body(
                command.path,
            )
            if body_result.failure:
                return r[bool].fail(body_result.error or "target body check failed")
            if body_result.value:
                return r[bool].fail(
                    f"{command.path}: comandos com target devem ser header-only",
                )
        condition_result = (
            FlextTestsMakeContractUtilitiesMixin.make_validate_mutation_conditions(
                command,
                param_by_name,
            )
        )
        if condition_result.failure:
            return r[bool].fail(condition_result.error or "mutates_when invalid")
        return r[bool].ok(True)

    @staticmethod
    def make_validate_mutation_conditions(
        command: m.Tests.MakeCommand,
        param_by_name: t.MappingKV[str, m.Tests.MakeParam],
    ) -> p.Result[bool]:
        """Validate conditional mutation predicates against declared parameters."""
        if not command.mutates_when:
            return r[bool].ok(True)
        apply_param = param_by_name.get(c.Tests.MAKE_APPLY_PARAM)
        if (
            apply_param is None
            or c.Tests.MAKE_DISPATCH_ENV_VALUE not in apply_param.choices
        ):
            return r[bool].fail(
                f"{command.path}: mutates_when exige APPLY com choice Y",
            )
        for condition in command.mutates_when:
            param = param_by_name.get(condition.name)
            if param is None:
                return r[bool].fail(
                    f"{command.path}: mutates_when referencia parametro ausente "
                    f"{condition.name}",
                )
            if param.choices:
                missing = tuple(
                    value for value in condition.values if value not in param.choices
                )
                if missing:
                    return r[bool].fail(
                        f"{command.path}: mutates_when.{condition.name} possui "
                        f"valores fora de choices: {','.join(missing)}",
                    )
        return r[bool].ok(True)


__all__: list[str] = ["FlextTestsMakeContractUtilitiesMixin"]
