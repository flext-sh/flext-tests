"""Unit tests for flext_tests.files module.

The part modules are imported as modules so pytest collects each behavioural
slice exactly once, through the composed suite below.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from tests.unit._files import (
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
    file_models.TestsFlextTestsModelsFiles,
    creation.TestsFlextTestsFilesCreation,
    info_cleanup.TestsFlextTestsFilesInfoCleanup,
    formats.TestsFlextTestsFilesFormats,
    read.TestsFlextTestsFilesRead,
    compare.TestsFlextTestsFilesCompare,
    info_metadata.TestsFlextTestsFilesInfoMetadata,
    contexts.TestsFlextTestsFilesContexts,
    content_meta.TestsFlextTestsFilesContentMeta,
    assert_exists.TestsFlextTestsFilesAssertExists,
    batch_create_in.TestsFlextTestsFilesBatchCreateIn,
):
    """Test suite for FlextTestsFiles.FileInfo model."""
