from datetime import datetime
from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.api.deps import get_db
from app.main import app


class FakeDeviceService:
    def __init__(self, db):
        self.db = db

    def update_device(self, device_id, request):
        assert device_id == 7
        assert request.name == "updated"
        return SimpleNamespace(
            id=device_id,
            name=request.name,
            ip_address="192.168.1.10",
            ssh_port=22,
            username="admin",
            monitoring_enabled=True,
            status="ONLINE",
            last_seen=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )


def override_get_db():
    return object()


def test_update_device_route_accepts_patch(monkeypatch):
    monkeypatch.setattr(
        "app.api.v1.routes.device_routes.DeviceService", FakeDeviceService
    )
    app.dependency_overrides[get_db] = override_get_db

    try:
        client = TestClient(app)
        response = client.patch(
            "/api/v1/devices/7",
            json={"name": "updated", "monitoring_enabled": True},
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert response.json()["name"] == "updated"
    assert response.json()["monitoring_enabled"] is True
