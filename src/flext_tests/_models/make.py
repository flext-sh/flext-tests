"""Models for the generic Make command framework.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import TYPE_CHECKING, Annotated

from flext_cli import m, u

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsMakeModelsMixin:
    """Pydantic models for registry-driven Make command metadata."""

    class MakeParam(m.Value):
        """One environment-backed command parameter."""

        name: Annotated[str, u.Field(description="Environment variable name.")]
        help: Annotated[str, u.Field(description="Human-readable parameter help.")]
        required: Annotated[
            bool,
            u.Field(description="Whether the parameter is required."),
        ] = False
        default: Annotated[
            str,
            u.Field(description="Default value when the environment is unset."),
        ] = ""
        choices: Annotated[
            t.StrSequence,
            u.Field(description="Allowed values for the parameter."),
        ] = ()

    class MakeMutationCondition(m.Value):
        """One environment-backed conditional mutation predicate."""

        name: Annotated[str, u.Field(description="Environment variable name.")]
        values: Annotated[
            t.StrSequence,
            u.Field(description="Values that make the command mutating."),
        ]

    class MakeCommand(m.Value):
        """One promoted command discovered from a flext-command header."""

        verb: Annotated[str, u.Field(description="Canonical make verb.")]
        what: Annotated[str, u.Field(description="Canonical WHAT value.")]
        domain: Annotated[str, u.Field(description="Functional command domain.")]
        summary: Annotated[str, u.Field(description="Short help summary.")]
        description: Annotated[str, u.Field(description="Detailed help text.")]
        example: Annotated[str, u.Field(description="Canonical invocation example.")]
        path: Annotated[Path, u.Field(description="Source script path.")]
        mutates: Annotated[
            bool,
            u.Field(description="Whether execution can mutate workspace state."),
        ]
        mutates_when: Annotated[
            t.SequenceOf[FlextTestsMakeModelsMixin.MakeMutationCondition],
            u.Field(description="Conditional mutation predicates."),
        ] = ()
        aliases: Annotated[
            t.StrSequence,
            u.Field(description="Verb aliases declared on."),
        ] = ()
        params: Annotated[
            t.SequenceOf[FlextTestsMakeModelsMixin.MakeParam],
            u.Field(description="Environment-backed parameter contract."),
        ] = ()
        rules: Annotated[
            t.StrSequence,
            u.Field(description="Governance rules enforced by this command."),
        ] = ()
        target: Annotated[
            str,
            u.Field(description="Optional Make target for header-only commands."),
        ] = ""
        surface: Annotated[
            str,
            u.Field(
                description="Declared surface-validation route for Python commands.",
            ),
        ] = ""
        target_env: Annotated[
            t.StrPairSequence,
            u.Field(description="Environment overrides for target dispatch."),
        ] = ()

    class MakeRegistry(m.Value):
        """Discovered command registry keyed by verb and WHAT."""

        commands_by_verb: Annotated[
            t.MappingKV[str, t.MappingKV[str, FlextTestsMakeModelsMixin.MakeCommand]],
            u.Field(description="Commands keyed by verb then WHAT."),
        ]
        aliases_by_name: Annotated[
            t.MappingKV[str, str],
            u.Field(description="Verb aliases keyed by alias name."),
        ] = u.Field(default_factory=lambda: MappingProxyType(dict[str, str]()))

    class MakeSurfaceProbe(m.Value):
        """One in-process dispatcher probe for surface validation."""

        name: Annotated[str, u.Field(description="Stable probe name.")]
        argv: Annotated[t.StrSequence, u.Field(description="Dispatcher argv.")]
        env: Annotated[
            t.MappingKV[str, str],
            u.Field(description="Environment values for this probe."),
        ] = u.Field(default_factory=lambda: MappingProxyType(dict[str, str]()))
        expected_output: Annotated[
            t.StrSequence,
            u.Field(description="Output fragments expected from the probe."),
        ] = ()

    class MakeSurfaceProbeResult(m.Value):
        """Captured output from one dispatcher probe."""

        returncode: Annotated[int, u.Field(description="Dispatcher return code.")]
        stdout: Annotated[str, u.Field(description="Captured standard output.")] = ""
        stderr: Annotated[str, u.Field(description="Captured standard error.")] = ""


__all__: list[str] = ["FlextTestsMakeModelsMixin"]


# NOTE (import discipline): nested param models annotate through their
# enclosing mixin and through sibling mixins (TYPE_CHECKING-only imports)
# that are not yet bound while the class body executes — pydantic defers
# those models and its lazy rebuild resolves against the CALLING module's
# imports, which breaks consumers whose test modules import neither.
# Rebuild every nested model deterministically against the merged namespace
# of this module and every already-imported _models sibling.
import sys as _sys

_rebuild_ns = {
    k: v
    for _mod_name, _mod in tuple(_sys.modules.items())
    if _mod is not None
    and _mod_name in ("flext_tests",) or _mod_name.startswith("flext_tests._models.")
    for k, v in vars(_mod).items()
    if k.endswith("ModelsMixin") or k in ("t", "p", "m", "u", "c", "r", "s", "x")
}
_rebuild_ns.update(
    {
        k: v
        for k, v in vars(_sys.modules[__name__]).items()
        if k.endswith("ModelsMixin") or k in ("t", "p", "m", "u", "c", "r")
    },
)
for _mixin_name, _mixin in tuple(vars(_sys.modules[__name__]).items()):
    if not isinstance(_mixin, type) or not _mixin_name.endswith("ModelsMixin"):
        continue
    _rebuild_ns[_mixin_name] = _mixin
    for _member in tuple(vars(_mixin).values()):
        if isinstance(_member, type) and hasattr(_member, "model_rebuild"):
            _member.model_rebuild(_types_namespace=_rebuild_ns)
