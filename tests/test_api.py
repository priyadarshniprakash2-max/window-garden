import sys
from pathlib import Path
from itertools import count

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

import pytest
from fastapi.testclient import TestClient
import main


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(
        main,
        "plants",
        {
            1: main.Plant(id=1, name="Monstera", water_every_days=7),
            2: main.Plant(id=2, name="Snake plant", water_every_days=14),
            3: main.Plant(id=3, name="Basil", water_every_days=2),
        },
    )
    monkeypatch.setattr(main, "_ids", count(4))

    with TestClient(main.app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_list_plants(client):
    response = client.get("/api/plants")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_add_plant(client):
    response = client.post(
        "/api/plants",
        json={"name": "Rose", "water_every_days": 5},
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Rose"
    assert response.json()["id"] == 4


def test_water_plant(client):
    response = client.post("/api/plants/1/water")

    assert response.status_code == 200
    assert response.json()["last_watered"] is not None


def test_delete_plant(client):
    response = client.delete("/api/plants/1")

    assert response.status_code == 204

    plants_response = client.get("/api/plants")
    assert len(plants_response.json()) == 2


def test_water_nonexistent_plant(client):
    response = client.post("/api/plants/999/water")

    assert response.status_code == 404
