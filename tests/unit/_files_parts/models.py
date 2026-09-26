"""Private file model test mixins facade.

Canonical owner of the mixin is ``_files_parts.file_models``; this module keeps
the ``_files_parts.models`` import path and the ``m`` facet contract generated
for the parts package.
"""

from __future__ import annotations

from tests import m

from .file_models import TestsFlextTestsFilesModelsMixin


