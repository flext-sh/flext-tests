import pytest


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if "test_external" in item.name:
            callspec = getattr(item, "callspec", None)
            if callspec is None:
                continue
            item.add_marker(getattr(pytest.mark, callspec.params["marker"]))
            item.add_marker(pytest.mark.usefixtures("service"))


@pytest.fixture
def service() -> None:
    pytest.fail("service fixture executed")
