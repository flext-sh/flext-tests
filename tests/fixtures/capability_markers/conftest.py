import pytest


def pytest_collection_modifyitems(items):
    for item in items:
        if "test_external" in item.name:
            item.add_marker(getattr(pytest.mark, item.callspec.params["marker"]))
            item.add_marker(pytest.mark.usefixtures("service"))


@pytest.fixture
def service():
    pytest.fail("service fixture executed")
