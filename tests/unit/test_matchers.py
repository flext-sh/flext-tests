"""Unit tests for flext_tests.matchers module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from tests.unit._matchers_parts.data_driven import MatchersDataDrivenMixin
from tests.unit._matchers_parts.fail_constraints import MatchersFailConstraintsMixin
from tests.unit._matchers_parts.ok_constraints import MatchersOkConstraintsMixin
from tests.unit._matchers_parts.results import MatchersResultsMixin
from tests.unit._matchers_parts.scope_errors import MatchersScopeErrorsMixin
from tests.unit._matchers_parts.that_attrs import MatchersThatAttrsMixin
from tests.unit._matchers_parts.that_collections import MatchersThatCollectionsMixin
from tests.unit._matchers_parts.validation import MatchersValidationMixin

__all__ = ["TestsFlextTestsMatchers"]


class TestsFlextTestsMatchers(
    MatchersResultsMixin,
    MatchersValidationMixin,
    MatchersOkConstraintsMixin,
    MatchersFailConstraintsMixin,
    MatchersThatCollectionsMixin,
    MatchersThatAttrsMixin,
    MatchersScopeErrorsMixin,
    MatchersDataDrivenMixin,
):
    """Test suite for tm class."""
