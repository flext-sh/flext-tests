"""Unit tests for flext_tests.files module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._files_parts.assert_exists import FilesAssertExistsMixin
from ._files_parts.batch_create_in import FilesBatchCreateInMixin
from ._files_parts.compare import FilesCompareMixin
from ._files_parts.content_meta import FilesContentMetaMixin
from ._files_parts.contexts import FilesContextsMixin
from ._files_parts.creation import FilesCreationMixin
from ._files_parts.formats import FilesFormatsMixin
from ._files_parts.info_cleanup import FilesInfoCleanupMixin
from ._files_parts.info_metadata import FilesInfoMetadataMixin
from ._files_parts.models import FilesModelsMixin
from ._files_parts.read import FilesReadMixin


class TestsFlextTestsFiles(
    FilesModelsMixin,
    FilesCreationMixin,
    FilesInfoCleanupMixin,
    FilesFormatsMixin,
    FilesReadMixin,
    FilesCompareMixin,
    FilesInfoMetadataMixin,
    FilesContextsMixin,
    FilesContentMetaMixin,
    FilesAssertExistsMixin,
    FilesBatchCreateInMixin,
):
    """Test suite for FlextTestsFiles.FileInfo model."""
