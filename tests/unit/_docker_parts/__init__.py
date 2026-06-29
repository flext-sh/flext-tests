# AUTO-GENERATED FILE — Regenerate with: make gen
"""Docker Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import (
        c as c,
        d as d,
        e as e,
        h as h,
        m as m,
        p as p,
        r as r,
        s as s,
        t as t,
        td as td,
        tf as tf,
        tk as tk,
        tm as tm,
        tv as tv,
        u as u,
        x as x,
    )
    from tests.unit._docker_parts.builders import (
        DockerBuildersMixin as DockerBuildersMixin,
    )
    from tests.unit._docker_parts.operations import (
        DockerOperationsMixin as DockerOperationsMixin,
    )
    from tests.unit._docker_parts.state import DockerStateMixin as DockerStateMixin
    from tests.unit._docker_parts.targets import (
        DockerTargetsMixin as DockerTargetsMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".builders": ("DockerBuildersMixin",),
        ".operations": ("DockerOperationsMixin",),
        ".state": ("DockerStateMixin",),
        ".targets": ("DockerTargetsMixin",),
        "flext_tests": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "td",
            "tf",
            "tk",
            "tm",
            "tv",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
