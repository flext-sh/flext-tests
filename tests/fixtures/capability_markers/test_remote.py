import pytest


@pytest.mark.parametrize("marker", ("remote", "connectivity"))
def test_external(marker, request):
    pytest.fail("test executed")


@pytest.mark.integration
def test_pure_integration():
    pass
