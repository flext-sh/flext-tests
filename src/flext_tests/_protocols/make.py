"""Protocol-of-model contracts for the generic Make command framework."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from flext_tests import t


# NOTE (multi-agent): keep runtime Make result specializations protocol-first.
class FlextTestsProtocolsMake:
    """Read-only structural contracts published under ``p.Tests``."""

    @runtime_checkable
    class MakeParam(Protocol):
        """Environment-backed Make command parameter."""

        @property
        def name(self) -> str: ...

        @property
        def help(self) -> str: ...

        @property
        def required(self) -> bool: ...

        @property
        def default(self) -> str: ...

        @property
        def choices(self) -> t.StrSequence: ...

    @runtime_checkable
    class MakeMutationCondition(Protocol):
        """Environment-backed conditional mutation predicate."""

        @property
        def name(self) -> str: ...

        @property
        def values(self) -> t.StrSequence: ...

    @runtime_checkable
    class MakeCommand(Protocol):
        """Promoted command discovered from a Make command header."""

        @property
        def verb(self) -> str: ...

        @property
        def what(self) -> str: ...

        @property
        def domain(self) -> str: ...

        @property
        def summary(self) -> str: ...

        @property
        def description(self) -> str: ...

        @property
        def example(self) -> str: ...

        @property
        def path(self) -> Path: ...

        @property
        def mutates(self) -> bool: ...

        @property
        def mutates_when(
            self,
        ) -> t.SequenceOf[FlextTestsProtocolsMake.MakeMutationCondition]: ...

        @property
        def aliases(self) -> t.StrSequence: ...

        @property
        def params(self) -> t.SequenceOf[FlextTestsProtocolsMake.MakeParam]: ...

        @property
        def rules(self) -> t.StrSequence: ...

        @property
        def target(self) -> str: ...

        @property
        def target_env(self) -> t.StrPairSequence: ...

    @runtime_checkable
    class MakeRegistry(Protocol):
        """Discovered command registry keyed by verb and WHAT value."""

        @property
        def commands_by_verb(
            self,
        ) -> t.MappingKV[
            str, t.MappingKV[str, FlextTestsProtocolsMake.MakeCommand]
        ]: ...

        @property
        def aliases_by_name(self) -> t.MappingKV[str, str]: ...


__all__: tuple[str, ...] = ("FlextTestsProtocolsMake",)
