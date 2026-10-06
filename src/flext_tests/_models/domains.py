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


# NOTE (import discipline): nested models annotate through sibling modules and
# TYPE_CHECKING-only imports whose names are invisible to a nested class body;
# complete them here against the merged namespace (own globals + base module +
# package aliases), tolerating the rare still-unresolvable annotation (it
# stays deferred exactly as before instead of crashing the import).
import sys as _sys

_rebuild_ns: dict = dict(globals())
try:
    _rebuild_ns.update(vars(_sys.modules["flext_tests._models.base"]))
except KeyError:
    pass
for _alias in ("t", "p", "m", "u", "c", "r", "s", "x"):
    try:
        _rebuild_ns.setdefault(_alias, getattr(_sys.modules["flext_tests"], _alias))
    except AttributeError:
        pass

for _mixin_name in tuple(globals()):
    _mixin = globals().get(_mixin_name)
    if isinstance(_mixin, type) and _mixin_name.endswith("ModelsMixin"):
        for _member in tuple(vars(_mixin).values()):
            if isinstance(_member, type) and hasattr(_member, "model_rebuild"):
                _member.model_rebuild(_types_namespace=_rebuild_ns, raise_errors=False)
