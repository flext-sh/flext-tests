"""Behavioral contract for the in-process ASGI GET helper.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from tests import t, tm, u


class TestsFlextTestsHttp:
    """Exercise only the public request/response behavior."""

    @staticmethod
    def test_get_captures_json_status_and_content_type() -> None:
        """A JSON route returns the typed body, text and media type."""
        response = u.Tests.http_get(TestsFlextTestsHttp._json_app, "/health")

        tm.that(response.status_code, eq=200)
        tm.that(response.content_type, eq="application/json")
        tm.that(response.text, eq='{"status": "ok"}')
        tm.that(response.json_body, eq={"status": "ok"})

    @staticmethod
    def test_get_leaves_json_empty_for_plain_text() -> None:
        """A text route keeps the parsed JSON body unset."""
        response = u.Tests.http_get(TestsFlextTestsHttp._text_app, "/info")

        tm.that(response.status_code, eq=200)
        tm.that(response.content_type, eq="text/plain")
        tm.that(response.text, eq="ready")
        tm.that(response.json_body, none=True)

    @staticmethod
    async def _lifespan(
        receive: t.Tests.AsgiReceive,
        send: t.Tests.AsgiSend,
    ) -> None:
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return

    @staticmethod
    async def _json_app(
        scope: t.Tests.AsgiScope,
        receive: t.Tests.AsgiReceive,
        send: t.Tests.AsgiSend,
    ) -> None:
        if scope["type"] == "lifespan":
            await TestsFlextTestsHttp._lifespan(receive, send)
            return
        del scope, receive
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"application/json")],
        })
        await send({
            "type": "http.response.body",
            "body": b'{"status": "ok"}',
        })

    @staticmethod
    async def _text_app(
        scope: t.Tests.AsgiScope,
        receive: t.Tests.AsgiReceive,
        send: t.Tests.AsgiSend,
    ) -> None:
        if scope["type"] == "lifespan":
            await TestsFlextTestsHttp._lifespan(receive, send)
            return
        del scope, receive
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        })
        await send({
            "type": "http.response.body",
            "body": b"ready",
        })
