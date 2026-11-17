# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_tests/_protocols/http
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_tests import t


class FlextTestsProtocolsHttp:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class HttpResponse(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def status_code(self) -> int:
            """HTTP status code."""
            ...

        @property
        def content_type(self) -> str:
            """Response media type."""
            ...

        @property
        def text(self) -> str:
            """Decoded response body."""
            ...

        @property
        def json_body(self) -> t.JsonValue | None:
            """Parsed JSON body when the response is JSON."""
            ...


__all__: list[str] = [
    "FlextTestsProtocolsHttp",
]
