import pytest

from fastapi.testclient import TestClient

from app.dependencies import room_manager, storage
from app.main import app


@pytest.fixture(name="client")
def client_fixture() -> TestClient:
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True)
def clear_storage() -> None:
    storage.tasks.clear()
    storage.next_id = 1
    room_manager.rooms.clear()
