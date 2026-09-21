# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit. Matchers Parts package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .data_driven import TestsFlextTestsMatchersDataDriven
    from .fail_constraints import TestsFlextTestsMatchersFailConstraints
    from .ok_constraints import TestsFlextTestsMatchersOkConstraints
    from .predicates import TestsFlextTestsMatchersPredicates
    from .rejects_assignment import (
        TestsFlextTestsMatchersRejectsAssignment,
        _Frozen,
        _Mutable,
        _PluginType,
    )
    from .results import TestsFlextTestsMatchersResults
    from .scope_errors import TestsFlextTestsMatchersScopeErrors
    from .that_attrs import TestsFlextTestsMatchersThatAttrs
    from .that_collections import TestsFlextTestsMatchersThatCollections
    from .validation import TestsFlextTestsMatchersValidation
__all__: tuple[str, ...] = (
    "TestsFlextTestsMatchersDataDriven",
    "TestsFlextTestsMatchersFailConstraints",
    "TestsFlextTestsMatchersOkConstraints",
    "TestsFlextTestsMatchersPredicates",
    "TestsFlextTestsMatchersRejectsAssignment",
    "TestsFlextTestsMatchersResults",
    "TestsFlextTestsMatchersScopeErrors",
    "TestsFlextTestsMatchersThatAttrs",
    "TestsFlextTestsMatchersThatCollections",
    "TestsFlextTestsMatchersValidation",
    "_Frozen",
    "_Mutable",
    "_PluginType",
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
            ".data_driven": ("TestsFlextTestsMatchersDataDriven",),
            ".fail_constraints": ("TestsFlextTestsMatchersFailConstraints",),
            ".ok_constraints": ("TestsFlextTestsMatchersOkConstraints",),
            ".predicates": ("TestsFlextTestsMatchersPredicates",),
            ".rejects_assignment": (
                "TestsFlextTestsMatchersRejectsAssignment",
                "_Frozen",
                "_Mutable",
                "_PluginType",
            ),
            ".results": ("TestsFlextTestsMatchersResults",),
            ".scope_errors": ("TestsFlextTestsMatchersScopeErrors",),
            ".that_attrs": ("TestsFlextTestsMatchersThatAttrs",),
            ".that_collections": ("TestsFlextTestsMatchersThatCollections",),
            ".validation": ("TestsFlextTestsMatchersValidation",),
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
