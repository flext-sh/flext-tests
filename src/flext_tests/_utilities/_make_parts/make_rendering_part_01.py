"""Rendering helper utilities for flext-tests Make command metadata."""

from __future__ import annotations

from collections.abc import Iterable

from flext_tests import m
from flext_tests._utilities.make_registry import FlextTestsMakeRegistryUtilitiesMixin


class FlextTestsMakeRenderingUtilitiesMixin(FlextTestsMakeRegistryUtilitiesMixin):
    """Render registry-driven Make helper fragments."""

    @staticmethod
    def make_format_params_inline(params: Iterable[m.Tests.MakeParam]) -> str:
        """Render command params in one compact inline form."""
        parts: list[str] = []
        for param in params:
            suffix = "*" if param.required else ""
            detail: list[str] = []
            if param.default:
                detail.append(f"default={param.default}")
            if param.choices:
                detail.append(f"choices={','.join(param.choices)}")
            rendered = f"{param.name}{suffix}"
            if detail:
                rendered = f"{rendered}({';'.join(detail)})"
            parts.append(rendered)
        return ", ".join(parts)

    @staticmethod
    def make_mutation_marker(command: m.Tests.MakeCommand) -> str:
        """Return the compact mutation marker for verb help."""
        if command.mutates:
            return " [mutates]"
        if command.mutates_when:
            return " [conditional-mutates]"
        return ""

    @staticmethod
    def make_mutation_label(command: m.Tests.MakeCommand) -> str:
        """Return the reader-facing mutation label for command help."""
        if command.mutates:
            return "sim"
        if command.mutates_when:
            return "condicional"
        return "nao"

    @staticmethod
    def make_format_mutation_conditions(
        conditions: Iterable[m.Tests.MakeMutationCondition],
    ) -> str:
        """Render conditional mutation predicates compactly."""
        return "; ".join(
            f"{condition.name}={('|'.join(condition.values))}"
            for condition in conditions
        )

    @staticmethod
    def make_example_for(command: m.Tests.MakeCommand, requested_verb: str) -> str:
        """Return the example adjusted for an alias-preserving verb."""
        example: str = command.example
        canonical = f"make {command.verb}"
        requested = f"make {requested_verb}"
        if example.startswith(canonical):
            return requested + example[len(canonical) :]
        return example


__all__: list[str] = ["FlextTestsMakeRenderingUtilitiesMixin"]
