import pytest

from flext_tests import c


@pytest.mark.parametrize("marker", c.Tests.CONNECTIVITY_MARKERS)
def test_external(marker: str, request: pytest.FixtureRequest) -> None:
    pytest.fail("test executed")
