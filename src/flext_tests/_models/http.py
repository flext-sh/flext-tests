"""In-process HTTP response models for route tests.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import m

from flext_tests import t


class FlextTestsModelsHttp:
    """HTTP response model group (status, content type, text and JSON body)."""

    class HttpResponse(m.Value):
        """Response captured from one in-process ASGI request."""

        status_code: Annotated[int, m.Field(description="HTTP status code.")]
        content_type: Annotated[
            str,
            m.Field(description="Response media type."),
        ]
        text: Annotated[str, m.Field(description="Decoded response body.")]
        json_body: Annotated[
            t.JsonValue | None,
            m.Field(description="Parsed JSON body when the response is JSON."),
        ] = None


__all__ = ["FlextTestsModelsHttp"]
