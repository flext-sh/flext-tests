# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit. Files Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .assert_exists import FilesAssertExistsMixin
    from .batch_create_in import FilesBatchCreateInMixin
    from .compare import FilesCompareMixin
    from .content_meta import FilesContentMetaMixin
    from .contexts import FilesContextsMixin
    from .creation import FilesCreationMixin
    from .formats import FilesFormatsMixin
    from .info_cleanup import FilesInfoCleanupMixin
    from .info_metadata import FilesInfoMetadataMixin
    from .models import FilesModelsMixin
    from .read import FilesReadMixin
__all__: tuple[str, ...] = (
    "FilesAssertExistsMixin",
    "FilesBatchCreateInMixin",
    "FilesCompareMixin",
    "FilesContentMetaMixin",
    "FilesContextsMixin",
    "FilesCreationMixin",
    "FilesFormatsMixin",
    "FilesInfoCleanupMixin",
    "FilesInfoMetadataMixin",
    "FilesModelsMixin",
    "FilesReadMixin",
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
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
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
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
