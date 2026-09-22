"""Unit tests for flext_tests.files module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._files_parts.assert_exists import TestsFlextTestsFilesAssertExistsMixin
from ._files_parts.batch_create_in import TestsFlextTestsFilesBatchCreateInMixin
from ._files_parts.compare import TestsFlextTestsFilesCompareMixin
from ._files_parts.content_meta import TestsFlextTestsFilesContentMetaMixin
from ._files_parts.contexts import TestsFlextTestsFilesContextsMixin
from ._files_parts.creation import TestsFlextTestsFilesCreationMixin
from ._files_parts.formats import TestsFlextTestsFilesFormatsMixin
from ._files_parts.info_cleanup import TestsFlextTestsFilesInfoCleanupMixin
from ._files_parts.info_metadata import TestsFlextTestsFilesInfoMetadataMixin
from ._files_parts.models import TestsFlextTestsFilesModelsMixin
from ._files_parts.read import TestsFlextTestsFilesReadMixin


class TestsFlextTestsFiles(
    TestsFlextTestsFilesModelsMixin,
    TestsFlextTestsFilesCreationMixin,
    TestsFlextTestsFilesInfoCleanupMixin,
    TestsFlextTestsFilesFormatsMixin,
    TestsFlextTestsFilesReadMixin,
    TestsFlextTestsFilesCompareMixin,
    TestsFlextTestsFilesInfoMetadataMixin,
    TestsFlextTestsFilesContextsMixin,
    TestsFlextTestsFilesContentMetaMixin,
    TestsFlextTestsFilesAssertExistsMixin,
    TestsFlextTestsFilesBatchCreateInMixin,
):
    """Test suite for FlextTestsFiles.FileInfo model."""
