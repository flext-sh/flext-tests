"""Rendering utilities for flext-tests Make command metadata."""

from __future__ import annotations

from flext_tests import c, m, p, r, t
from flext_tests._utilities._make_parts.make_rendering_part_01 import (
    FlextTestsMakeRenderingUtilitiesMixin as FlextTestsMakeRenderingUtilitiesMixinPart01,
)
from flext_tests._utilities.make_registry import FlextTestsMakeRegistryUtilitiesMixin


class FlextTestsMakeRenderingUtilitiesMixin(
    FlextTestsMakeRenderingUtilitiesMixinPart01
):
    """Render registry-driven Make help and dry-run output."""

    @staticmethod
    def make_render_global_help(registry: m.Tests.MakeRegistry) -> str:
        """Render top-level dispatcher help."""
        lines = ["flext - make <verbo> WHAT=<acao> [PARAM=value ...]", ""]
        for verb in FlextTestsMakeRegistryUtilitiesMixin.make_registry_verbs(registry):
            command = registry.commands_by_verb[verb][c.Tests.MAKE_DEFAULT_COMMAND]
            aliases = FlextTestsMakeRegistryUtilitiesMixin.make_registry_aliases_for(
                registry,
                verb,
            )
            suffix = f" (alias: {', '.join(aliases)})" if aliases else ""
            lines.append(f"  {verb:14} [{command.domain:12}] {command.summary}{suffix}")
        lines.extend((
            "",
            "Use: make <verbo> para lista os WHAT disponiveis.",
            "Use: make <verbo> WHAT=<acao> para executar.",
            "Use: make <verbo> WHAT=<verbo>/<acao> para help da acao.",
            "Comandos mutadores exigem APPLY=Y.",
        ))
        return "\n".join(lines)

    @staticmethod
    def make_render_verb_help(
        registry: m.Tests.MakeRegistry,
        requested_verb: str,
    ) -> p.Result[str]:
        """Render help for one promoted verb."""
        verb_result = FlextTestsMakeRegistryUtilitiesMixin.make_registry_resolve_verb(
            registry,
            requested_verb,
        )
        if verb_result.failure:
            return r[str].fail(verb_result.error or "verb unknown")
        verb = verb_result.value
        aliases = FlextTestsMakeRegistryUtilitiesMixin.make_registry_aliases_for(
            registry,
            verb,
        )
        alias_suffix = f" (alias: {', '.join(aliases)})" if aliases else ""
        lines = [
            f"make {requested_verb} WHAT=<WHAT>{alias_suffix}",
            "",
            "WHAT disponiveis:",
        ]
        commands = registry.commands_by_verb[verb]
        for what, command in sorted(commands.items()):
            marker = FlextTestsMakeRenderingUtilitiesMixin.make_mutation_marker(command)
            lines.append(f"  {what:20} [{command.domain:12}] {command.summary}{marker}")
        command_params = [
            (what, command)
            for what, command in sorted(commands.items())
            if command.params
        ]
        if command_params:
            lines.extend(("", "Opcoes por WHAT:"))
            for what, command in command_params:
                rendered = (
                    FlextTestsMakeRenderingUtilitiesMixin.make_format_params_inline(
                        command.params
                    )
                )
                lines.append(f"  {what:20} {rendered}")
            lines.extend((
                "",
                "Detalhe de uma acao:",
                f"  make {requested_verb} WHAT={requested_verb}/<WHAT>",
                f"  make {requested_verb} WHAT=<WHAT> OPTIONS=Y",
            ))
        rules = sorted({
            rule for command in commands.values() for rule in command.rules
        })
        if rules:
            lines.extend(("", "Regras:"))
            lines.extend(f"  - {rule}" for rule in rules)
        examples = sorted({
            FlextTestsMakeRenderingUtilitiesMixin.make_example_for(
                command,
                requested_verb,
            )
            for command in commands.values()
        })
        if examples:
            lines.extend(("", "Exemplos:"))
            lines.extend(f"  {example}" for example in examples)
        return r[str].ok("\n".join(lines))

    @staticmethod
    def make_render_command_help(
        registry: m.Tests.MakeRegistry,
        requested_verb: str,
        what: str,
    ) -> p.Result[str]:
        """Render help for one promoted command."""
        command_result = FlextTestsMakeRegistryUtilitiesMixin.make_registry_command(
            registry,
            requested_verb,
            what,
        )
        if command_result.failure:
            return r[str].fail(command_result.error or "command unknown")
        command = command_result.value
        lines = [
            f"make {requested_verb} WHAT={what}",
            "",
            f"Dominio: {command.domain}",
            f"Mutacao: {FlextTestsMakeRenderingUtilitiesMixin.make_mutation_label(command)}",
        ]
        if command.mutates:
            lines.append("Sem APPLY=Y a execucao fica em dry-run.")
        elif command.mutates_when:
            conditions = (
                FlextTestsMakeRenderingUtilitiesMixin.make_format_mutation_conditions(
                    command.mutates_when
                )
            )
            lines.append(f"Mutacao condicional: {conditions}.")
        lines.extend(("", command.summary, command.description))
        if command.params:
            lines.extend(("", "Parametros:"))
            for param in command.params:
                required = " obrigatorio" if param.required else ""
                default = f" default={param.default}" if param.default else ""
                choices = f" choices={','.join(param.choices)}" if param.choices else ""
                lines.append(
                    f"  {param.name:24} {param.help}{required}{default}{choices}"
                )
        if command.rules:
            lines.extend(("", "Regras:"))
            lines.extend(f"  - {rule}" for rule in command.rules)
        lines.extend((
            "",
            "Exemplo:",
            f"  {FlextTestsMakeRenderingUtilitiesMixin.make_example_for(command, requested_verb)}",
        ))
        return r[str].ok("\n".join(lines))

    @staticmethod
    def make_render_dry_run(
        command: m.Tests.MakeCommand,
        requested_verb: str,
        what: str,
        env: t.MappingKV[str, str],
    ) -> str:
        """Render dry-run output for one mutating command."""
        lines = [
            "DRY-RUN: nenhuma mutacao executada.",
            f"Comando: make {requested_verb} WHAT={what}",
            f"Dominio: {command.domain}",
            f"Resumo: {command.summary}",
            "Regra: comando mutador exige APPLY=Y.",
        ]
        if command.params:
            lines.extend(("", "Parametros atuais:"))
            for param in command.params:
                value = FlextTestsMakeRegistryUtilitiesMixin.make_param_value(
                    param,
                    command,
                    env,
                )
                shown = value or "<ausente>"
                required = "obrigatorio" if param.required else "opcional"
                choices = f" choices={','.join(param.choices)}" if param.choices else ""
                lines.append(
                    f"  {param.name:24} {shown:20} {required}{choices} - {param.help}"
                )
        lines.extend((
            "",
            "Execucao canonica:",
            f"  {FlextTestsMakeRenderingUtilitiesMixin.make_example_for(command, requested_verb)}",
        ))
        return "\n".join(lines)


__all__: list[str] = ["FlextTestsMakeRenderingUtilitiesMixin"]
