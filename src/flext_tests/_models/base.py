"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Self

from flext_infra import m, p, u

from flext_tests import t


def _entity_payload_default() -> FlextTestsBaseModelsMixin.Payload:
    """Late-bound entity default.

    Defined before the mixin so the class body binds the bare name while the
    mixin itself resolves only at instantiation time: annotations stay lazy
    under ``from __future__ import annotations`` and this function's body
    runs after the module is complete. A lambda here would be flattened back
    into an eager attribute reference by the fleet's autofix pass, which
    re-introduces the class-body NameError.
    """
    return FlextTestsBaseModelsMixin.Payload.atom_default()


def _payload_entries_default() -> t.Tests.PayloadEntries[
    FlextTestsBaseModelsMixin.Payload
]:
    """Late-bound empty mapping arm, bound the same way as the entity default."""
    return MappingProxyType({})


class FlextTestsBaseModelsMixin:
    class Payload(m.ArbitraryTypesModel):
        """Owned native payload tree; model leaves retain their instance identity."""

        kind: Annotated[
            t.Tests.PayloadKind, m.Field(frozen=True, description="Native value arm.")
        ]
        atom: Annotated[
            t.Tests.PayloadAtom | p.Model | None,
            m.Field(
                frozen=True,
                description="Native scalar or model instance; never a JSON dump.",
            ),
        ] = None
        items: Annotated[
            t.Tests.PayloadItems[Self],
            m.Field(
                frozen=True,
                description="Ordered children; kind retains the source collection.",
            ),
        ] = ()
        entries: Annotated[
            t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload],
            m.Field(
                default_factory=_payload_entries_default,
                frozen=True,
                description="String-keyed payload children.",
            ),
        ]

        @u.field_validator("entries", mode="after")
        @classmethod
        def freeze_entries(
            cls, value: t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload]
        ) -> t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload]:
            """Own an immutable copy so caller mutation cannot invalidate the arm."""
            return MappingProxyType(dict(value))

        @u.model_validator(mode="after")
        def validate_arm(self) -> Self:
            """Reject data in fields belonging to a different native value arm."""
            if self.kind == "atom":
                if self.items or self.entries:
                    msg = "An atom payload cannot contain children"
                    raise ValueError(msg)
            elif self.kind == "mapping":
                if self.atom is not None or self.items:
                    msg = "A mapping payload cannot contain an atom or items"
                    raise ValueError(msg)
            elif self.atom is not None or self.entries:
                msg = "A collection payload cannot contain an atom or entries"
                raise ValueError(msg)
            return self

        @classmethod
        def atom_default(cls) -> FlextTestsBaseModelsMixin.Payload:
            """Build the default atom payload used by entity value defaults."""
            return cls(kind="atom")

    class Entity(m.Entity):
        """Factory entity class for tests."""

        name: Annotated[str, m.Field(description="Entity display name.")] = ""
        value: Annotated[
            FlextTestsBaseModelsMixin.Payload,
            m.Field(description="Arbitrary serializable payload."),
        ] = m.Field(default_factory=_entity_payload_default)

    class Value(m.Value):
        """Factory value object class for tests."""

        data: Annotated[str, m.Field(description="Payload data string.")] = ""
        count: Annotated[int, m.Field(description="Occurrence counter.")] = 0
