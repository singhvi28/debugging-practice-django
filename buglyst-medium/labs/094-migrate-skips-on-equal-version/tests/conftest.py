import pytest

from helper import reset


@pytest.fixture(autouse=True)
def _reset_schema():
    reset()
    yield
    reset()
