"""Public test-matchers facade for flext-tests.

Short alias: ``tm`` (test matchers). Re-exports the matcher utilities from the
private ``_utilities.matchers`` implementation so the root ``flext_tests``
package can publish ``tm`` as a governed root facade alias.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_tests._utilities import FlextTestsUtilitiesMatchers

# A fachada e o proprio namespace: a dupla indirecao Tests.Matchers foi
# removida pela onda de achatamento; that/fail/ok vivem direto aqui.
tm = FlextTestsUtilitiesMatchers
"""Public test-matchers facade alias for flext_tests."""

__all__: list[str] = ["FlextTestsUtilitiesMatchers", "tm"]
