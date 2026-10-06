"""Test-namespace models for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from flext_cli import m, u

from flext_tests._constants.namespace import FlextTestsConstantsNamespace

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsNamespaceModelsMixin:
    class TestNamespace(m.Value):
        """Collision-free namespace token for one test run and one worker.

        The token mixes a base36 epoch stamp, the checkout identity, the
        worker code, and random bytes, so parallel pytest processes on the
        same host (and reruns after a reseeding plugin) never share a
        namespace.
        """

        token: Annotated[
            str,
            u.Field(
                pattern=FlextTestsConstantsNamespace.NAMESPACE_TOKEN_PATTERN,
                description="Lowercase namespace token (23 chars).",
            ),
        ]
        run_token: Annotated[
            str,
            u.Field(description="Shared token of the whole pytest run."),
        ]
        worker: Annotated[
            str,
            u.Field(description="Worker identifier (master outside xdist)."),
        ]
        checkout: Annotated[
            str,
            u.Field(description="Checkout identity digest prefix."),
        ]
        issued_at_ns: Annotated[
            int,
            u.Field(ge=0, description="Issue time in nanoseconds."),
        ]
        root: Annotated[
            t.NonEmptyStr,
            u.Field(description="Absolute checkout root path."),
        ]


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
