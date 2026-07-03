# AUTO-GENERATED FILE — Regenerate with: make gen
"""Matchers Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests.tests.unit._matchers_parts.data_driven import (
        MatchersDataDrivenMixin as MatchersDataDrivenMixin,
    )
    from flext_tests.tests.unit._matchers_parts.fail_constraints import (
        MatchersFailConstraintsMixin as MatchersFailConstraintsMixin,
    )
    from flext_tests.tests.unit._matchers_parts.ok_constraints import (
        MatchersOkConstraintsMixin as MatchersOkConstraintsMixin,
    )
    from flext_tests.tests.unit._matchers_parts.predicates import (
        MatchersPredicates as MatchersPredicates,
    )
    from flext_tests.tests.unit._matchers_parts.results import (
        MatchersResultsMixin as MatchersResultsMixin,
    )
    from flext_tests.tests.unit._matchers_parts.scope_errors import (
        MatchersScopeErrorsMixin as MatchersScopeErrorsMixin,
    )
    from flext_tests.tests.unit._matchers_parts.that_attrs import (
        MatchersThatAttrsMixin as MatchersThatAttrsMixin,
    )
    from flext_tests.tests.unit._matchers_parts.that_collections import (
        MatchersThatCollectionsMixin as MatchersThatCollectionsMixin,
    )
    from flext_tests.tests.unit._matchers_parts.validation import (
        MatchersValidationMixin as MatchersValidationMixin,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".data_driven": ("MatchersDataDrivenMixin",),
        ".fail_constraints": ("MatchersFailConstraintsMixin",),
        ".ok_constraints": ("MatchersOkConstraintsMixin",),
        ".predicates": ("MatchersPredicates",),
        ".results": ("MatchersResultsMixin",),
        ".scope_errors": ("MatchersScopeErrorsMixin",),
        ".that_attrs": ("MatchersThatAttrsMixin",),
        ".that_collections": ("MatchersThatCollectionsMixin",),
        ".validation": ("MatchersValidationMixin",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
