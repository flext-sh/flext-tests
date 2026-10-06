"""Container-spec models for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from flext_cli import m, u

if TYPE_CHECKING:
    from flext_tests import t
    from flext_tests._models.docker import FlextTestsDockerModelsMixin


class FlextTestsSpecModelsMixin:
    class ContainerSpec(m.Value):
        """Declarative spec of the containers one suite needs.

        One YAML document feeds both the pre-test CLI (`flext-tests docker
        ensure|verify|down --spec ...`) and the in-session plugin — a single
        SSOT so provisioning outside the pytest deadline and the in-session
        capability never diverge.
        """

        containers: Annotated[
            t.MutableMappingKV[str, FlextTestsDockerModelsMixin.ContainerConfig],
            u.Field(
                description=(
                    "Target name → container config; the target name is what "
                    "CLI --target and the in-session plugin resolve."
                ),
            ),
        ]
        initializer_command: Annotated[
            str | None,
            u.Field(
                description=(
                    "Optional shell command run once after ensure, receiving "
                    "the container environment readback as env vars."
                ),
            ),
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
