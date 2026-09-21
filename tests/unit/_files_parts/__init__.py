# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit. Files Parts package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .assert_exists import TestsFlextTestsFilesAssertExists
    from .batch_create_in import TestsFlextTestsFilesBatchCreateIn
    from .compare import TestsFlextTestsFilesCompare
    from .content_meta import TestsFlextTestsFilesContentMeta
    from .contexts import TestsFlextTestsFilesContexts
    from .creation import TestsFlextTestsFilesCreation
    from .formats import TestsFlextTestsFilesFormats
    from .info_cleanup import TestsFlextTestsFilesInfoCleanup
    from .info_metadata import TestsFlextTestsFilesInfoMetadata
    from .models import TestsFlextTestsFilesModels
    from .read import TestsFlextTestsFilesRead
__all__: tuple[str, ...] = (
    "TestsFlextTestsFilesAssertExists",
    "TestsFlextTestsFilesBatchCreateIn",
    "TestsFlextTestsFilesCompare",
    "TestsFlextTestsFilesContentMeta",
    "TestsFlextTestsFilesContexts",
    "TestsFlextTestsFilesCreation",
    "TestsFlextTestsFilesFormats",
    "TestsFlextTestsFilesInfoCleanup",
    "TestsFlextTestsFilesInfoMetadata",
    "TestsFlextTestsFilesModels",
    "TestsFlextTestsFilesRead",
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
            ".assert_exists": ("TestsFlextTestsFilesAssertExists",),
            ".batch_create_in": ("TestsFlextTestsFilesBatchCreateIn",),
            ".compare": ("TestsFlextTestsFilesCompare",),
            ".content_meta": ("TestsFlextTestsFilesContentMeta",),
            ".contexts": ("TestsFlextTestsFilesContexts",),
            ".creation": ("TestsFlextTestsFilesCreation",),
            ".formats": ("TestsFlextTestsFilesFormats",),
            ".info_cleanup": ("TestsFlextTestsFilesInfoCleanup",),
            ".info_metadata": ("TestsFlextTestsFilesInfoMetadata",),
            ".models": ("TestsFlextTestsFilesModels",),
            ".read": ("TestsFlextTestsFilesRead",),
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
