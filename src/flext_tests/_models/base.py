"""Models extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Any, Self

from flext_cli import m, p
from pydantic import field_validator, model_validator

# Runtime import: the nested models' field annotations reference ``t.Tests.*``
# names, and pydantic resolves field annotations at runtime. A TYPE_CHECKING-only
# import leaves the names unresolvable, deferring the models forever (PydanticUserError:
# not fully defined). The package-level lazy descriptor resolves ``t`` without cycles.
from flext_tests import t


def _entity_payload_default() -> (
    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
):
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
    return FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload.atom_default()


class FlextTestsFlextModelsBase:
    """Canonical namespace owner."""

    @staticmethod
    def _payload_entries_default() -> t.Tests.PayloadEntries[
        FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
    ]:
        """Late-bound empty mapping arm, bound the same way as the entity default.

        Returns:
            The resulting ``t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload]``.
        """
        return MappingProxyType({})

    class FlextTestsBaseModelsMixin:
        class Payload(m.ArbitraryTypesModel):
            """Owned native payload tree.

            Model leaves retain their instance identity.
            """

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
                t.Tests.PayloadEntries[
                    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
                ],
                m.Field(
                    default_factory=dict,
                    frozen=True,
                    description="String-keyed payload children.",
                ),
            ]

            @field_validator("entries", mode="after")
            @classmethod
            def freeze_entries(
                cls,
                value: t.Tests.PayloadEntries[
                    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
                ],
            ) -> t.Tests.PayloadEntries[
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload
            ]:
                """Own an immutable copy so caller mutation cannot invalidate the arm.

                Returns:
                    The resulting
                        ``t.Tests.PayloadEntries[FlextTestsBaseModelsMixin.Payload]``.
                """
                return MappingProxyType(dict(value))

            @model_validator(mode="after")
            def validate_arm(self) -> Self:
                """Reject data in fields belonging to a different native value arm.

                Returns:
                    The resulting ``Self``.

                Raises:
                    ValueError: If an atom payload contains children; if a mapping
                        payload contains an atom or items; or if a collection payload
                        contains an atom or entries.
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
            def atom_default(
                cls,
            ) -> FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload:
                """Build the default atom payload used by entity value defaults.

                Returns:
                    The resulting ``FlextTestsBaseModelsMixin.Payload``.
                """
                return cls(kind="atom")

        class Entity(m.Entity):
            """Factory entity class for tests."""

            name: Annotated[str, m.Field(description="Entity display name.")] = ""
            value: Annotated[
                FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
                m.Field(description="Arbitrary serializable payload."),
            ] = m.Field(default_factory=_entity_payload_default)

        class Value(m.Value):
            """Factory value object class for tests."""

            data: Annotated[str, m.Field(description="Payload data string.")] = ""
            count: Annotated[int, m.Field(description="Occurrence counter.")] = 0


# Nested models capture their enclosing class-body frame as the pydantic
# parent namespace, which cannot see module-level names while the module is
# still executing; their field schemas therefore stay deferred (mock
# validators) and would raise ``not fully defined`` at first use. Completing
# them here, once the full module namespace is bound, keeps every declaration
# strictly resolved before the facade exposes it.
_base_module_ns: dict[str, Any] = dict(globals())
for _nested_model in (
    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Entity,
    FlextTestsFlextModelsBase.FlextTestsBaseModelsMixin.Payload,
):
    if not _nested_model.__pydantic_fields_complete__:
        _nested_model.model_rebuild(_types_namespace=_base_module_ns)


__all__: list[str] = ["FlextTestsFlextModelsBase"]
