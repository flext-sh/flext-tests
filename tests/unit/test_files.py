"""Unit tests for flext_tests.files module.

The part modules are imported as modules so pytest collects each behavioural
slice exactly once, through the composed suite below.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from ._files_parts import (
    assert_exists,
    batch_create_in,
    compare,
    content_meta,
    contexts,
    creation,
    file_models,
    formats,
    info_cleanup,
    info_metadata,
    read,
)


class TestsFlextTestsFiles(
    file_models.TestsFlextTestsFilesModelsMixin,
    creation.TestsFlextTestsFilesCreationMixin,
    info_cleanup.TestsFlextTestsFilesInfoCleanupMixin,
    formats.TestsFlextTestsFilesFormatsMixin,
    read.TestsFlextTestsFilesReadMixin,
    compare.TestsFlextTestsFilesCompareMixin,
    info_metadata.TestsFlextTestsFilesInfoMetadataMixin,
    contexts.TestsFlextTestsFilesContextsMixin,
    content_meta.TestsFlextTestsFilesContentMetaMixin,
    assert_exists.TestsFlextTestsFilesAssertExistsMixin,
    batch_create_in.TestsFlextTestsFilesBatchCreateInMixin,
):
    """Test suite for FlextTestsFiles.FileInfo model."""
