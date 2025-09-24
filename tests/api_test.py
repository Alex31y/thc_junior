import pytest
from fastapi.testclient import TestClient
from catalogue.api import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_manufacturers(client: TestClient) -> None:
    response = client.get("/manufacturers")
    assert response.status_code == 200

