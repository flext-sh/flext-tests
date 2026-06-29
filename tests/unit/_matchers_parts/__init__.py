# AUTO-GENERATED FILE — Regenerate with: make gen
"""Matchers Parts package."""

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
    from tests.unit._matchers_parts.data_driven import (
        MatchersDataDrivenMixin as MatchersDataDrivenMixin,
    )
    from tests.unit._matchers_parts.fail_constraints import (
        MatchersFailConstraintsMixin as MatchersFailConstraintsMixin,
    )
    from tests.unit._matchers_parts.ok_constraints import (
        MatchersOkConstraintsMixin as MatchersOkConstraintsMixin,
    )
    from tests.unit._matchers_parts.results import (
        MatchersResultsMixin as MatchersResultsMixin,
    )
    from tests.unit._matchers_parts.scope_errors import (
        MatchersScopeErrorsMixin as MatchersScopeErrorsMixin,
    )
    from tests.unit._matchers_parts.that_attrs import (
        MatchersThatAttrsMixin as MatchersThatAttrsMixin,
    )
    from tests.unit._matchers_parts.that_collections import (
        MatchersThatCollectionsMixin as MatchersThatCollectionsMixin,
    )
    from tests.unit._matchers_parts.validation import (
        MatchersValidationMixin as MatchersValidationMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".data_driven": ("MatchersDataDrivenMixin",),
        ".fail_constraints": ("MatchersFailConstraintsMixin",),
        ".ok_constraints": ("MatchersOkConstraintsMixin",),
        ".predicates": ("predicates",),
        ".results": ("MatchersResultsMixin",),
        ".scope_errors": ("MatchersScopeErrorsMixin",),
        ".that_attrs": ("MatchersThatAttrsMixin",),
        ".that_collections": ("MatchersThatCollectionsMixin",),
        ".validation": ("MatchersValidationMixin",),
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
