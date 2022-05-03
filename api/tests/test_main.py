from fastapi.testclient import TestClient
import pytest

# FIXME: We should do create_app instead
from api.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_get_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "description": "An API built to interact with BIOS synchronized data."
    }
