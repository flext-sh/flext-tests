# AUTO-GENERATED FILE — Regenerate with: make gen
"""Files package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._assertions": ("FlextTestsFilesAssertionsMixin",),
        "._batch": ("FlextTestsFilesBatchMixin",),
        "._comparison": ("FlextTestsFilesComparisonMixin",),
        "._contexts": ("FlextTestsFilesContextsMixin",),
        "._creation": ("FlextTestsFilesCreationMixin",),
        "._info": ("FlextTestsFilesInfoMixin",),
        "._lifecycle": ("FlextTestsFilesLifecycleMixin",),
        "._reading": ("FlextTestsFilesReadingMixin",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
