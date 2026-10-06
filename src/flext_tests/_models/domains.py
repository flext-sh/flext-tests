"""Domain model extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_core import m


class FlextTestsDomainModelsMixin:
    """Domain-model namespace mixin."""

    class HandlerCaseSpec(m.FrozenModel):
        """Test handler case specification."""

        handler_id: Annotated[str, m.Field(description="Unique handler identifier.")]
        handler_type: Annotated[
            str,
            m.Field(description="Handler implementation kind."),
        ]
        description: Annotated[str, m.Field(description="Human-readable summary.")]
        expected_result: Annotated[
            str | None,
            m.Field(description="Expected outcome label."),
        ] = None
        should_fail: Annotated[
            bool,
            m.Field(description="Whether the case must raise."),
        ] = False
        error_message: Annotated[
            str | None,
            m.Field(description="Expected error text."),
        ] = None


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
