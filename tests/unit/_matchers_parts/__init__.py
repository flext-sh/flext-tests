# AUTO-GENERATED FILE — Regenerate with: make gen
"""Matchers Parts package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

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
