from fastapi.testclient import TestClient
import pytest

# FIXME: We should do create_app instead
from api.main import DatabaseConfig, create_app, db_config


@pytest.fixture
def fake_settings():
    def get_fake_settings():
        return DatabaseConfig(host="not a real host", port="xyz", name="testdatabase")

    return get_fake_settings


@pytest.fixture()
def app(fake_settings):
    app = create_app()
    app.dependency_overrides[db_config] = fake_settings
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_get_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "description": "An API built to interact with BIOS synchronized data."
    }


def test_get_items(client: TestClient):
    # Since we're not running an actual test database
    with pytest.raises(ValueError):
        client.get("/test/items")
