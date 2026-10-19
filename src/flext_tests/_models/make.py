"""Models for the generic Make command framework.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import Annotated

from flext_cli import m

from flext_tests import t


class FlextTestsMakeModelsMixin:
    """Pydantic models for registry-driven Make command metadata."""

    class MakeParam(m.Value):
        """One environment-backed command parameter."""

        name: Annotated[str, m.Field(description="Environment variable name.")]
        help: Annotated[str, m.Field(description="Human-readable parameter help.")]
        required: Annotated[
            bool,
            m.Field(description="Whether the parameter is required."),
        ] = False
        default: Annotated[
            str,
            m.Field(description="Default value when the environment is unset."),
        ] = ""
        choices: Annotated[
            t.StrSequence,
            m.Field(description="Allowed values for the parameter."),
        ] = ()

    class MakeMutationCondition(m.Value):
        """One environment-backed conditional mutation predicate."""

        name: Annotated[str, m.Field(description="Environment variable name.")]
        values: Annotated[
            t.StrSequence,
            m.Field(description="Values that make the command mutating."),
        ]

    class MakeCommand(m.Value):
        """One promoted command discovered from a flext-command header."""

        verb: Annotated[str, m.Field(description="Canonical make verb.")]
        what: Annotated[str, m.Field(description="Canonical WHAT value.")]
        domain: Annotated[str, m.Field(description="Functional command domain.")]
        summary: Annotated[str, m.Field(description="Short help summary.")]
        description: Annotated[str, m.Field(description="Detailed help text.")]
        example: Annotated[str, m.Field(description="Canonical invocation example.")]
        path: Annotated[Path, m.Field(description="Source script path.")]
        mutates: Annotated[
            bool,
            m.Field(description="Whether execution can mutate workspace state."),
        ]
        mutates_when: Annotated[
            t.SequenceOf[FlextTestsMakeModelsMixin.MakeMutationCondition],
            m.Field(description="Conditional mutation predicates."),
        ] = ()
        aliases: Annotated[
            t.StrSequence,
            m.Field(description="Verb aliases declared on."),
        ] = ()
        params: Annotated[
            t.SequenceOf[FlextTestsMakeModelsMixin.MakeParam],
            m.Field(description="Environment-backed parameter contract."),
        ] = ()
        rules: Annotated[
            t.StrSequence,
            m.Field(description="Governance rules enforced by this command."),
        ] = ()
        target: Annotated[
            str,
            m.Field(description="Optional Make target for header-only commands."),
        ] = ""
        surface: Annotated[
            str,
            m.Field(
                description="Declared surface-validation route for Python commands.",
            ),
        ] = ""
        target_env: Annotated[
            t.StrPairSequence,
            m.Field(description="Environment overrides for target dispatch."),
        ] = ()

    class MakeRegistry(m.Value):
        """Discovered command registry keyed by verb and WHAT."""

        commands_by_verb: Annotated[
            t.MappingKV[str, t.MappingKV[str, FlextTestsMakeModelsMixin.MakeCommand]],
            m.Field(description="Commands keyed by verb then WHAT."),
        ]
        aliases_by_name: Annotated[
            t.MappingKV[str, str],
            m.Field(description="Verb aliases keyed by alias name."),
        ] = m.Field(default_factory=lambda: MappingProxyType(dict[str, str]()))

    class MakeSurfaceProbe(m.Value):
        """One in-process dispatcher probe for surface validation."""

        name: Annotated[str, m.Field(description="Stable probe name.")]
        argv: Annotated[t.StrSequence, m.Field(description="Dispatcher argv.")]
        env: Annotated[
            t.MappingKV[str, str],
            m.Field(description="Environment values for this probe."),
        ] = m.Field(default_factory=lambda: MappingProxyType(dict[str, str]()))
        expected_output: Annotated[
            t.StrSequence,
            m.Field(description="Output fragments expected from the probe."),
        ] = ()

    class MakeSurfaceProbeResult(m.Value):
        """Captured output from one dispatcher probe."""

        returncode: Annotated[int, m.Field(description="Dispatcher return code.")]
        stdout: Annotated[str, m.Field(description="Captured standard output.")] = ""
        stderr: Annotated[str, m.Field(description="Captured standard error.")] = ""


__all__: list[str] = ["FlextTestsMakeModelsMixin"]
