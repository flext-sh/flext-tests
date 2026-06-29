"""Registry discovery utilities for flext-tests Make commands."""

from __future__ import annotations

from flext_tests import m, p, r, t
from flext_tests._utilities.make_contract import FlextTestsMakeContractUtilitiesMixin


class FlextTestsMakeRegistryUtilitiesMixin(FlextTestsMakeContractUtilitiesMixin):
    """Assemble registry-driven Make commands."""

    @staticmethod
    def _make_add_command(
        commands_by_verb: t.MutableMappingKV[
            str,
            t.MutableMappingKV[str, m.Tests.MakeCommand],
        ],
        aliases_by_name: t.MutableMappingKV[str, str],
        command: m.Tests.MakeCommand,
    ) -> p.Result[bool]:
        """Add one command to mutable registry assembly state."""
        by_what = commands_by_verb.setdefault(command.verb, {})
        if command.what in by_what:
            return r[bool].fail(
                f"comando duplicado: {command.verb} WHAT={command.what}"
            )
        by_what[command.what] = command
        for alias in command.aliases:
            previous = aliases_by_name.get(alias)
            if previous and previous != command.verb:
                return r[bool].fail(
                    f"alias duplicado: {alias} aponta para {previous} e {command.verb}"
                )
            aliases_by_name[alias] = command.verb
        return r[bool].ok(True)


__all__: list[str] = ["FlextTestsMakeRegistryUtilitiesMixin"]
