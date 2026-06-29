# AUTO-GENERATED FILE — Regenerate with: make gen
"""Files Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import (
        c as c,
        d as d,
        e as e,
        h as h,
        m as m,
        p as p,
        r as r,
        s as s,
        t as t,
        td as td,
        tf as tf,
        tk as tk,
        tm as tm,
        tv as tv,
        u as u,
        x as x,
    )
    from tests.unit._files_parts.assert_exists import (
        FilesAssertExistsMixin as FilesAssertExistsMixin,
    )
    from tests.unit._files_parts.batch_create_in import (
        FilesBatchCreateInMixin as FilesBatchCreateInMixin,
    )
    from tests.unit._files_parts.compare import FilesCompareMixin as FilesCompareMixin
    from tests.unit._files_parts.content_meta import (
        FilesContentMetaMixin as FilesContentMetaMixin,
    )
    from tests.unit._files_parts.contexts import (
        FilesContextsMixin as FilesContextsMixin,
    )
    from tests.unit._files_parts.creation import (
        FilesCreationMixin as FilesCreationMixin,
    )
    from tests.unit._files_parts.formats import FilesFormatsMixin as FilesFormatsMixin
    from tests.unit._files_parts.info_cleanup import (
        FilesInfoCleanupMixin as FilesInfoCleanupMixin,
    )
    from tests.unit._files_parts.info_metadata import (
        FilesInfoMetadataMixin as FilesInfoMetadataMixin,
    )
    from tests.unit._files_parts.models import FilesModelsMixin as FilesModelsMixin
    from tests.unit._files_parts.read import FilesReadMixin as FilesReadMixin
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".assert_exists": ("FilesAssertExistsMixin",),
        ".batch_create_in": ("FilesBatchCreateInMixin",),
        ".compare": ("FilesCompareMixin",),
        ".content_meta": ("FilesContentMetaMixin",),
        ".contexts": ("FilesContextsMixin",),
        ".creation": ("FilesCreationMixin",),
        ".formats": ("FilesFormatsMixin",),
        ".info_cleanup": ("FilesInfoCleanupMixin",),
        ".info_metadata": ("FilesInfoMetadataMixin",),
        ".models": ("FilesModelsMixin",),
        ".read": ("FilesReadMixin",),
        "flext_tests": (
            "c",
            "d",
            "e",
            "h",
            "m",
            "p",
            "r",
            "s",
            "t",
            "td",
            "tf",
            "tk",
            "tm",
            "tv",
            "u",
            "x",
        ),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
