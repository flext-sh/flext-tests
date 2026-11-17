"""In-process HTTP requests against ASGI applications.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib import import_module

from flext_tests import m, t


class FlextTestsUtilitiesHttp:
    """Exercise ASGI routes in-process without a client in the consumer."""

    @staticmethod
    def http_get(app: t.Tests.AsgiApp, path: str) -> m.Tests.HttpResponse:
        """Issue a GET against ``app`` and capture the typed response.

        The client is loaded only when a test calls this method, so importing
        the utilities facade never loads the HTTP stack.

        Args:
            app: The ASGI application to exercise.
            path: The request path, including any query string.

        Returns:
            The status, content type, text and parsed JSON body when present.

        """
        client_type = import_module("starlette.testclient").TestClient
        with client_type(app) as client:
            response = client.get(path)
            content_type = response.headers.get("content-type", "")
            return m.Tests.HttpResponse(
                status_code=response.status_code,
                content_type=content_type,
                text=response.text,
                json_body=response.json() if "json" in content_type else None,
            )


__all__ = ["FlextTestsUtilitiesHttp"]
