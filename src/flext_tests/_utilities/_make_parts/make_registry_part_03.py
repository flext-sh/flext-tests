"""Registry discovery and header loading for flext-tests Make commands."""

from __future__ import annotations

from pathlib import Path

from flext_tests import c, m, p, r, t
from flext_tests._utilities._make_parts.make_registry_part_02 import (
    FlextTestsMakeRegistryUtilitiesMixin as FlextTestsMakeRegistryUtilitiesMixinPart02,
)
from flext_tests._utilities.make_contract import FlextTestsMakeContractUtilitiesMixin
from flext_tests._utilities.make_parsing import FlextTestsMakeParsingUtilitiesMixin


class FlextTestsMakeRegistryUtilitiesMixin(FlextTestsMakeRegistryUtilitiesMixinPart02):
    """Discover and load registry-driven Make commands."""

    @classmethod
    def make_discover(cls, scripts_dir: Path) -> p.Result[m.Tests.MakeRegistry]:
        """Discover and validate promoted commands under ``scripts/cmd``."""
        if not scripts_dir.exists():
            return r[m.Tests.MakeRegistry].fail("diretorio scripts/cmd ausente")

        commands_by_verb: t.MutableMappingKV[
            str,
            t.MutableMappingKV[str, m.Tests.MakeCommand],
        ] = {}
        aliases_by_name: t.MutableMappingKV[str, str] = {}
        for verb_dir in sorted(scripts_dir.iterdir(), key=lambda item: item.name):
            if (
                not verb_dir.is_dir()
                or verb_dir.name in c.Tests.MAKE_IGNORED_COMMAND_DIRS
            ):
                continue
            for path in sorted(verb_dir.iterdir(), key=lambda item: item.name):
                if path.name == "__pycache__":
                    continue
                load_result = cls.make_load_command(
                    path,
                    verb_dir.name,
                )
                if load_result.failure:
                    return r[m.Tests.MakeRegistry].fail(
                        load_result.error or "command load failed",
                    )
                add_result = cls._make_add_command(
                    commands_by_verb,
                    aliases_by_name,
                    load_result.value,
                )
                if add_result.failure:
                    return r[m.Tests.MakeRegistry].fail(
                        add_result.error or "command registration failed",
                    )

        registry = m.Tests.MakeRegistry(
            commands_by_verb=commands_by_verb,
            aliases_by_name=aliases_by_name,
        )
        validate_result = FlextTestsMakeContractUtilitiesMixin.make_validate_registry(
            registry,
        )
        if validate_result.failure:
            return r[m.Tests.MakeRegistry].fail(
                validate_result.error or "registry validation failed",
            )
        return r[m.Tests.MakeRegistry].ok(registry)

    @classmethod
    def make_load_command(
        cls,
        path: Path,
        expected_verb: str,
    ) -> p.Result[m.Tests.MakeCommand]:
        """Load one promoted command from its flext-command TOML header."""
        if path.name == "__pycache__":
            return r[m.Tests.MakeCommand].fail(f"{path}: cache publico invalido")
        if path.is_dir():
            return r[m.Tests.MakeCommand].fail(
                f"{path}: diretorio publico nao pode estar aninhado",
            )
        if path.suffix not in c.Tests.MAKE_COMMAND_SUFFIXES:
            return r[m.Tests.MakeCommand].fail(
                f"{path}: arquivo publico deve ser .sh ou .py",
            )
        data_result = FlextTestsMakeParsingUtilitiesMixin.make_header_data(path)
        if data_result.failure:
            return r[m.Tests.MakeCommand].fail(
                data_result.error or "header load failed",
            )
        data = data_result.value
        verb_result = FlextTestsMakeParsingUtilitiesMixin.make_require_string(
            data,
            "verb",
            path,
        )
        what_result = FlextTestsMakeParsingUtilitiesMixin.make_require_string(
            data,
            "what",
            path,
        )
        if verb_result.failure:
            return r[m.Tests.MakeCommand].fail(verb_result.error or "verb missing")
        if what_result.failure:
            return r[m.Tests.MakeCommand].fail(what_result.error or "what missing")
        verb = verb_result.value
        what = what_result.value
        if verb != expected_verb:
            return r[m.Tests.MakeCommand].fail(
                f"{path}: header verb={verb} diverge do diretorio {expected_verb}",
            )
        if what != path.stem:
            return r[m.Tests.MakeCommand].fail(
                f"{path}: header what={what} diverge do arquivo {path.stem}",
            )
        return cls._make_command_from_data(
            path,
            data,
            verb,
            what,
        )


__all__: list[str] = ["FlextTestsMakeRegistryUtilitiesMixin"]
