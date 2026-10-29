import os
from pathlib import Path

import pytest

from flext_tests import c


@pytest.mark.docker
def test_isolated_environment(docker_test_environment: Path) -> None:
    assert docker_test_environment.name == ".env"
    assert not (Path(__file__).parent / ".env").exists()
    declared = docker_test_environment.read_text(encoding="utf-8").strip()
    name, value = declared.split(c.Tests.DOCKER_ENV_SEPARATOR, 1)
    assert os.environ[name] == value
