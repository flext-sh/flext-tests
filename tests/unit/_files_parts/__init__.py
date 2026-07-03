# AUTO-GENERATED FILE — Regenerate with: make gen
"""Files Parts package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

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
