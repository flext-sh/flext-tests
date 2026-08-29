# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit. Matchers Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .data_driven import MatchersDataDrivenMixin
    from .fail_constraints import MatchersFailConstraintsMixin
    from .ok_constraints import MatchersOkConstraintsMixin
    from .predicates import MatchersPredicates
    from .rejects_assignment import MatchersRejectsAssignmentMixin
    from .results import MatchersResultsMixin
    from .scope_errors import MatchersScopeErrorsMixin
    from .that_attrs import MatchersThatAttrsMixin
    from .that_collections import MatchersThatCollectionsMixin
    from .validation import MatchersValidationMixin
__all__: tuple[str, ...] = (
    "MatchersDataDrivenMixin",
    "MatchersFailConstraintsMixin",
    "MatchersOkConstraintsMixin",
    "MatchersPredicates",
    "MatchersRejectsAssignmentMixin",
    "MatchersResultsMixin",
    "MatchersScopeErrorsMixin",
    "MatchersThatAttrsMixin",
    "MatchersThatCollectionsMixin",
    "MatchersValidationMixin",
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
            ".data_driven": ("MatchersDataDrivenMixin",),
            ".fail_constraints": ("MatchersFailConstraintsMixin",),
            ".ok_constraints": ("MatchersOkConstraintsMixin",),
            ".predicates": ("MatchersPredicates",),
            ".rejects_assignment": ("MatchersRejectsAssignmentMixin",),
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
