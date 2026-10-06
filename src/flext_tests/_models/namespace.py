"""Test-namespace models for flext_tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from flext_cli import m, u

from flext_tests._constants.namespace import FlextTestsConstantsNamespace

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsNamespaceModelsMixin:
    class TestNamespace(m.Value):
        """Collision-free namespace token for one test run and one worker.

        The token mixes a base36 epoch stamp, the checkout identity, the
        worker code, and random bytes, so parallel pytest processes on the
        same host (and reruns after a reseeding plugin) never share a
        namespace.
        """

        token: Annotated[
            str,
            u.Field(
                pattern=FlextTestsConstantsNamespace.NAMESPACE_TOKEN_PATTERN,
                description="Lowercase namespace token (23 chars).",
            ),
        ]
        run_token: Annotated[
            str,
            u.Field(description="Shared token of the whole pytest run."),
        ]
        worker: Annotated[
            str,
            u.Field(description="Worker identifier (master outside xdist)."),
        ]
        checkout: Annotated[
            str,
            u.Field(description="Checkout identity digest prefix."),
        ]
        issued_at_ns: Annotated[
            int,
            u.Field(ge=0, description="Issue time in nanoseconds."),
        ]
        root: Annotated[
            t.NonEmptyStr,
            u.Field(description="Absolute checkout root path."),
        ]


# NOTE (import discipline): see _rebuild.py — nested models annotate through
# their enclosing mixin and TYPE_CHECKING-only siblings; rebuild them here,
# at import end, so the lazy rebuild never depends on the caller's imports.
from flext_tests._models._rebuild import rebuild_nested_models as _rebuild_nested_models

_rebuild_nested_models(FlextTestsNamespaceModelsMixin)
