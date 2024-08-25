import pytest
from fastapi.testclient import TestClient

from do_know_fastapi.app import app


@pytest.fixture
def client():
    return TestClient(app)
