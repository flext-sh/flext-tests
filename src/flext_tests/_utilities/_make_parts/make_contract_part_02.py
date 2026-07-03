"""Registry resolver utilities for flext-tests Make commands."""

from __future__ import annotations

from flext_tests import c, m, p, r, t
from flext_tests._utilities._make_parts.make_contract_part_01 import (
    FlextTestsMakeContractUtilitiesMixin as FlextTestsMakeContractUtilitiesMixinPart01,
)


class FlextTestsMakeContractUtilitiesMixin(FlextTestsMakeContractUtilitiesMixinPart01):
    """Validate command registries and resolve registry entries."""

    @staticmethod
    def make_validate_registry(registry: m.Tests.MakeRegistry) -> p.Result[bool]:
        """Validate the complete discovered command registry."""
        if not registry.commands_by_verb:
            return r[bool].fail(
                "nenhum comando encontrado em scripts/cmd/<verbo>/<what>"
            )
        for verb, commands in sorted(registry.commands_by_verb.items()):
            if c.Tests.MAKE_DEFAULT_COMMAND not in commands:
                return r[bool].fail(
                    f"verbo '{verb}' sem WHAT={c.Tests.MAKE_DEFAULT_COMMAND}"
                )
            domains = {command.domain for command in commands.values()}
            if len(domains) != 1:
                valid = ", ".join(sorted(domains))
                return r[bool].fail(
                    f"verbo '{verb}' declara mais de um domain: {valid}"
                )
            for command in commands.values():
                command_result = FlextTestsMakeContractUtilitiesMixin.make_validate_registered_command(
                    command
                )
                if command_result.failure:
                    return r[bool].fail(
                        command_result.error or "command contract invalid"
                    )
            choices_result = (
                FlextTestsMakeContractUtilitiesMixin.make_validate_all_choices(
                    verb,
                    commands,
                )
            )
            if choices_result.failure:
                return r[bool].fail(choices_result.error or "choices invalid")
        return r[bool].ok(True)

    @staticmethod
    def make_validate_registered_command(
        command: m.Tests.MakeCommand,
    ) -> p.Result[bool]:
        """Validate one command inside a complete registry."""
        if command.what != c.Tests.MAKE_DEFAULT_COMMAND and command.aliases:
            return r[bool].fail(
                f"{command.path}: aliases podem ser declarados apenas em "
                f"WHAT={c.Tests.MAKE_DEFAULT_COMMAND}"
            )
        return FlextTestsMakeContractUtilitiesMixin.make_validate_command_contract(
            command
        )

    @staticmethod
    def make_validate_all_choices(
        verb: str,
        commands: t.MappingKV[str, m.Tests.MakeCommand],
    ) -> p.Result[bool]:
        """Validate WHAT choices declared by the verb default command."""
        all_command = commands[c.Tests.MAKE_DEFAULT_COMMAND]
        what_param = next(
            (
                param
                for param in all_command.params
                if param.name == c.Tests.MAKE_WHAT_PARAM
            ),
            None,
        )
        if what_param is None or not what_param.choices:
            return r[bool].ok(True)
        declared = tuple(sorted(what_param.choices))
        actual = tuple(sorted(commands))
        if declared != actual:
            return r[bool].fail(
                f"{all_command.path}: choices de WHAT divergem dos comandos promovidos "
                f"para {verb}: declared={','.join(declared)} actual={','.join(actual)}"
            )
        return r[bool].ok(True)

    @staticmethod
    def make_registry_verbs(registry: m.Tests.MakeRegistry) -> t.StrSequence:
        """Return promoted verbs in display order."""
        return tuple(sorted(registry.commands_by_verb))

    @staticmethod
    def make_registry_resolve_verb(
        registry: m.Tests.MakeRegistry,
        verb: str,
    ) -> p.Result[str]:
        """Resolve one verb or alias to its canonical verb."""
        resolved = registry.aliases_by_name.get(verb, verb)
        if resolved not in registry.commands_by_verb:
            return r[str].fail(f"verbo '{verb}' desconhecido")
        return r[str].ok(resolved)

    @staticmethod
    def make_registry_commands(
        registry: m.Tests.MakeRegistry,
        verb: str,
    ) -> p.Result[t.MappingKV[str, m.Tests.MakeCommand]]:
        """Return commands registered for one verb."""
        resolved = FlextTestsMakeContractUtilitiesMixin.make_registry_resolve_verb(
            registry,
            verb,
        )
        if resolved.failure:
            return r[t.MappingKV[str, m.Tests.MakeCommand]].fail(
                resolved.error or "verb unknown"
            )
        return r[t.MappingKV[str, m.Tests.MakeCommand]].ok(
            registry.commands_by_verb[resolved.value]
        )

    @staticmethod
    def make_registry_command(
        registry: m.Tests.MakeRegistry,
        verb: str,
        what: str,
    ) -> p.Result[m.Tests.MakeCommand]:
        """Return one command by verb and WHAT value."""
        commands_result = FlextTestsMakeContractUtilitiesMixin.make_registry_commands(
            registry,
            verb,
        )
        if commands_result.failure:
            return r[m.Tests.MakeCommand].fail(commands_result.error or "verb unknown")
        commands = commands_result.value
        command = commands.get(what)
        if command is None:
            valid = " ".join(sorted(commands))
            return r[m.Tests.MakeCommand].fail(
                f"WHAT='{what}' invalido para {verb}. Validos: {valid}"
            )
        return r[m.Tests.MakeCommand].ok(command)

    @staticmethod
    def make_registry_aliases_for(
        registry: m.Tests.MakeRegistry,
        verb: str,
    ) -> t.StrSequence:
        """Return aliases that resolve to one canonical verb."""
        return tuple(
            sorted(
                alias
                for alias, target in registry.aliases_by_name.items()
                if target == verb
            )
        )


__all__: list[str] = ["FlextTestsMakeContractUtilitiesMixin"]
