"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, Annotated, Self

from flext_cli import m, p, u

if TYPE_CHECKING:
    from flext_tests import t


def _entity_payload_default() -> FlextTestsBaseModelsMixin.Payload:
    """Late-bound entity default.

    Defined before the mixin so the class body binds the bare name while the
    mixin itself resolves only at instantiation time: annotations stay lazy
    under ``from __future__ import annotations`` and this function's body
    runs after the module is complete. A lambda here would be flattened back
    into an eager attribute reference by the fleet's autofix pass, which
    re-introduces the class-body NameError.

    Returns:
        The resulting ``FlextTestsBaseModelsMixin.Payload``.
    """
    return FlextTestsBaseModelsMixin.Payload.atom_default()


def _payload_entries_default() -> t.Tests.PayloadEntries[
    FlextTestsBaseModelsMixin.Payload
]:
    """Late-bound empty mapping arm, bound the same way as the entity default.

    Returns:
        The resulting ``t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload]``.
    """
    return MappingProxyType({})


class FlextTestsBaseModelsMixin:
    class Payload(m.ArbitraryTypesModel):
        """Owned native payload tree; model leaves retain their instance identity."""

        kind: Annotated[
            t.Tests.PayloadKind,
            m.Field(frozen=True, description="Native value arm."),
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
            cls,
            value: t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload],
        ) -> t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload]:
            """Own an immutable copy so caller mutation cannot invalidate the arm.

            Returns:
                The resulting
                    ``t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload]``.
            """
            return MappingProxyType(dict(value))

        @u.model_validator(mode="after")
        def validate_arm(self) -> Self:
            """Reject data in fields belonging to a different native value arm.

            Returns:
                The resulting ``Self``.

            Raises:
                ValueError: If An atom payload cannot contain children; or if A mapping
                    payload cannot contain an atom or items; or if A collection payload
                    cannot contain an atom or entries.
            """
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
            """Build the default atom payload used by entity value defaults.

            Returns:
                The resulting ``FlextTestsBaseModelsMixin.Payload``.
            """
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
