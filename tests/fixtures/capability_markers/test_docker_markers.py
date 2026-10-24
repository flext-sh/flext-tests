import pytest

from flext_tests import c


@pytest.mark.parametrize("marker", c.Tests.CONNECTIVITY_MARKERS)
def test_external(marker, request):
    pytest.fail("test executed")
