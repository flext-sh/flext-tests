"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Self

from flext_infra import m, p, u

# Why not `from flext_tests import t`: during the facade's first import,
# typings.py is still initializing and its module-level `t` momentarily holds
# FlextInfraTypes, so `FlextTestsBaseTypesMixin.*` resolves against a class that never has
# `Tests` and the AttributeError escapes pydantic's NameError-only deferral.
# The payload aliases are ownable directly from their defining mixin — the
# same objects `FlextTestsTypes.Tests` composes, without facade recursion.
from flext_tests._typings.base import FlextTestsBaseTypesMixin


class FlextTestsBaseModelsMixin:
    class Payload(m.ArbitraryTypesModel):
        """Owned native payload tree; model leaves retain their instance identity."""

        kind: Annotated[
            FlextTestsBaseTypesMixin.PayloadKind, m.Field(frozen=True, description="Native value arm.")
        ]
        atom: Annotated[
            FlextTestsBaseTypesMixin.PayloadAtom | p.Model | None,
            m.Field(
                frozen=True,
                description="Native scalar or model instance; never a JSON dump.",
            ),
        ] = None
        items: Annotated[
            FlextTestsBaseTypesMixin.PayloadItems[Self],
            m.Field(
                frozen=True,
                description="Ordered children; kind retains the source collection.",
            ),
        ] = ()
        entries: Annotated[
            FlextTestsBaseTypesMixin.PayloadEntries[Self],
            m.Field(frozen=True, description="String-keyed payload children."),
        ] = m.Field(default_factory=lambda: MappingProxyType({}))

        @u.field_validator("entries", mode="after")
        @classmethod
        def freeze_entries(
            cls, value: FlextTestsBaseTypesMixin.PayloadEntries[Self]
        ) -> FlextTestsBaseTypesMixin.PayloadEntries[Self]:
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

    class Entity(m.Entity):
        """Factory entity class for tests."""

        name: Annotated[str, m.Field(description="Entity display name.")] = ""
        value: Annotated[
            FlextTestsBaseModelsMixin.Payload,
            m.Field(description="Arbitrary serializable payload."),
        ] = m.Field(
            default_factory=lambda: FlextTestsBaseModelsMixin.Payload(kind="atom")
        )

    class Value(m.Value):
        """Factory value object class for tests."""

        data: Annotated[str, m.Field(description="Payload data string.")] = ""
        count: Annotated[int, m.Field(description="Occurrence counter.")] = 0
