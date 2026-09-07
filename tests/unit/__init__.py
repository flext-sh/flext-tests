# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from . import (
        _docker_parts as _docker_parts,
        _files_parts as _files_parts,
        _matchers_parts as _matchers_parts,
    )
    from .test_matchers import TestsFlextTestsMatchers
    from .test_public_facade import TestsFlextTestsPublicFacade
__all__: tuple[str, ...] = (
    "TestsFlextTestsMatchers",
    "TestsFlextTestsPublicFacade",
    "_docker_parts",
    "_files_parts",
    "_matchers_parts",
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
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._docker_parts": ("_docker_parts",),
            "._files_parts": ("_files_parts",),
            "._matchers_parts": ("_matchers_parts",),
            ".test_matchers": ("TestsFlextTestsMatchers",),
            ".test_public_facade": ("TestsFlextTestsPublicFacade",),
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
