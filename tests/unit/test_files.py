"""Unit tests for flext_tests.files module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._files_parts.assert_exists import TestsFlextTestsFilesAssertExists
from ._files_parts.batch_create_in import TestsFlextTestsFilesBatchCreateIn
from ._files_parts.compare import TestsFlextTestsFilesCompare
from ._files_parts.content_meta import TestsFlextTestsFilesContentMeta
from ._files_parts.contexts import TestsFlextTestsFilesContexts
from ._files_parts.creation import TestsFlextTestsFilesCreation
from ._files_parts.formats import TestsFlextTestsFilesFormats
from ._files_parts.info_cleanup import TestsFlextTestsFilesInfoCleanup
from ._files_parts.info_metadata import TestsFlextTestsFilesInfoMetadata
from ._files_parts.models import TestsFlextTestsFilesModels
from ._files_parts.read import TestsFlextTestsFilesRead


class TestsFlextTestsFiles(
    TestsFlextTestsFilesModels,
    TestsFlextTestsFilesCreation,
    TestsFlextTestsFilesInfoCleanup,
    TestsFlextTestsFilesFormats,
    TestsFlextTestsFilesRead,
    TestsFlextTestsFilesCompare,
    TestsFlextTestsFilesInfoMetadata,
    TestsFlextTestsFilesContexts,
    TestsFlextTestsFilesContentMeta,
    TestsFlextTestsFilesAssertExists,
    TestsFlextTestsFilesBatchCreateIn,
):
    """Test suite for FlextTestsFiles.FileInfo model."""

    class Tests:
        """flext-tests files test namespace."""
