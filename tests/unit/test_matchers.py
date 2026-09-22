"""Unit tests for flext_tests.matchers module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._matchers_parts.data_driven import TestsFlextTestsMatchersDataDrivenMixin
from ._matchers_parts.fail_constraints import (
    TestsFlextTestsMatchersFailConstraintsMixin,
)
from ._matchers_parts.ok_constraints import TestsFlextTestsMatchersOkConstraintsMixin
from ._matchers_parts.rejects_assignment import (
    TestsFlextTestsMatchersRejectsAssignmentMixin,
)
from ._matchers_parts.results import TestsFlextTestsMatchersResultsMixin
from ._matchers_parts.scope_errors import TestsFlextTestsMatchersScopeErrorsMixin
from ._matchers_parts.that_attrs import TestsFlextTestsMatchersThatAttrsMixin
from ._matchers_parts.that_collections import (
    TestsFlextTestsMatchersThatCollectionsMixin,
)
from ._matchers_parts.validation import TestsFlextTestsMatchersValidationMixin

__all__ = ["TestsFlextTestsMatchers"]


class TestsFlextTestsMatchers(
    TestsFlextTestsMatchersResultsMixin,
    TestsFlextTestsMatchersValidationMixin,
    TestsFlextTestsMatchersOkConstraintsMixin,
    TestsFlextTestsMatchersFailConstraintsMixin,
    TestsFlextTestsMatchersThatCollectionsMixin,
    TestsFlextTestsMatchersThatAttrsMixin,
    TestsFlextTestsMatchersScopeErrorsMixin,
    TestsFlextTestsMatchersRejectsAssignmentMixin,
    TestsFlextTestsMatchersDataDrivenMixin,
):
    """Test suite for tm class."""
