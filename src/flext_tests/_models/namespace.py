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
