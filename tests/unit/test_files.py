"""Unit tests for flext_tests.files module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from tests.unit._files_parts.assert_exists import FilesAssertExistsMixin
from tests.unit._files_parts.batch_create_in import FilesBatchCreateInMixin
from tests.unit._files_parts.compare import FilesCompareMixin
from tests.unit._files_parts.content_meta import FilesContentMetaMixin
from tests.unit._files_parts.contexts import FilesContextsMixin
from tests.unit._files_parts.creation import FilesCreationMixin
from tests.unit._files_parts.formats import FilesFormatsMixin
from tests.unit._files_parts.info_cleanup import FilesInfoCleanupMixin
from tests.unit._files_parts.info_metadata import FilesInfoMetadataMixin
from tests.unit._files_parts.models import FilesModelsMixin
from tests.unit._files_parts.read import FilesReadMixin


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
    """Test suite for tf.FileInfo model."""
