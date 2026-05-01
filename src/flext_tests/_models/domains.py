"""Domain model extraction for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

from flext_core import m, u
from flext_tests._typings.base import FlextTestsBaseTypesMixin


class FlextTestsDomainModelsMixin:
    class FixtureSpec(m.Value):
        """Canonical fixture payload descriptor for test scenarios."""

        group: Annotated[
            str,
            u.Field(description="Fixture server/domain group."),
        ] = ""
        kind: Annotated[
            str,
            u.Field(description="Fixture type/kind identifier."),
        ] = ""
        content: Annotated[
            str,
            u.Field(description="Loaded fixture content."),
        ] = ""
        path: Annotated[
            Path | None,
            u.Field(description="Absolute fixture path if available."),
        ] = None

    class FixturePair(m.Value):
        """Fixture identity pair without payload body."""

        group: Annotated[
            str,
            u.Field(description="Fixture server/domain group."),
        ] = ""
        kind: Annotated[
            str,
            u.Field(description="Fixture type/kind identifier."),
        ] = ""

    class DomainCase(m.Value):
        """Generic domain test case model for reusable case sets."""

        id: Annotated[
            str,
            u.Field(description="Stable test-case identifier."),
        ] = ""
        description: Annotated[
            str,
            u.Field(description="Human-readable case purpose."),
        ] = ""
        data: Annotated[
            FlextTestsBaseTypesMixin.TestobjectSerializable,
            u.Field(description="Input payload for the test case."),
        ] = None
        expected: Annotated[
            FlextTestsBaseTypesMixin.TestobjectSerializable,
            u.Field(description="Expected result payload for the test case."),
        ] = None
