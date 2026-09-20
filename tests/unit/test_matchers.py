"""Unit tests for flext_tests.matchers module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._matchers_parts.data_driven import TestsFlextTestsMatchersDataDriven
from ._matchers_parts.fail_constraints import TestsFlextTestsMatchersFailConstraints
from ._matchers_parts.ok_constraints import TestsFlextTestsMatchersOkConstraints
from ._matchers_parts.rejects_assignment import TestsFlextTestsMatchersRejectsAssignment
from ._matchers_parts.results import TestsFlextTestsMatchersResults
from ._matchers_parts.scope_errors import TestsFlextTestsMatchersScopeErrors
from ._matchers_parts.that_attrs import TestsFlextTestsMatchersThatAttrs
from ._matchers_parts.that_collections import TestsFlextTestsMatchersThatCollections
from ._matchers_parts.validation import TestsFlextTestsMatchersValidation

__all__ = ["TestsFlextTestsMatchers"]


class TestsFlextTestsMatchers(
    TestsFlextTestsMatchersResults,
    TestsFlextTestsMatchersValidation,
    TestsFlextTestsMatchersOkConstraints,
    TestsFlextTestsMatchersFailConstraints,
    TestsFlextTestsMatchersThatCollections,
    TestsFlextTestsMatchersThatAttrs,
    TestsFlextTestsMatchersScopeErrors,
    TestsFlextTestsMatchersRejectsAssignment,
    TestsFlextTestsMatchersDataDriven,
):
    """Test suite for tm class."""

    class Tests:
        """flext-tests matchers test namespace."""
