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
