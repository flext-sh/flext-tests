# AUTO-GENERATED FILE — Regenerate with: make gen
"""Files Parts package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests.tests.unit._files_parts.assert_exists import (
        FilesAssertExistsMixin as FilesAssertExistsMixin,
    )
    from flext_tests.tests.unit._files_parts.batch_create_in import (
        FilesBatchCreateInMixin as FilesBatchCreateInMixin,
    )
    from flext_tests.tests.unit._files_parts.compare import (
        FilesCompareMixin as FilesCompareMixin,
    )
    from flext_tests.tests.unit._files_parts.content_meta import (
        FilesContentMetaMixin as FilesContentMetaMixin,
    )
    from flext_tests.tests.unit._files_parts.contexts import (
        FilesContextsMixin as FilesContextsMixin,
    )
    from flext_tests.tests.unit._files_parts.creation import (
        FilesCreationMixin as FilesCreationMixin,
    )
    from flext_tests.tests.unit._files_parts.formats import (
        FilesFormatsMixin as FilesFormatsMixin,
    )
    from flext_tests.tests.unit._files_parts.info_cleanup import (
        FilesInfoCleanupMixin as FilesInfoCleanupMixin,
    )
    from flext_tests.tests.unit._files_parts.info_metadata import (
        FilesInfoMetadataMixin as FilesInfoMetadataMixin,
    )
    from flext_tests.tests.unit._files_parts.models import (
        FilesModelsMixin as FilesModelsMixin,
    )
    from flext_tests.tests.unit._files_parts.read import (
        FilesReadMixin as FilesReadMixin,
    )
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
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
