import pytest
from fastapi.testclient import TestClient

from app.api.deps import get_db
from app.main import app


def test_get_db_yields_a_sqlalchemy_session():
    db_generator = get_db()
    db = next(db_generator)

    assert hasattr(db, "query")

    db.close()

    with pytest.raises(StopIteration):
        next(db_generator)


def test_login_route_returns_token_payload(monkeypatch):
    def fake_login(self, username, password):
        return "test-token"

    monkeypatch.setattr("app.services.auth_service.AuthService.login", fake_login)

    client = TestClient(app)
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "admin", "password": "password"},
    )

    assert response.status_code == 200
    assert response.json() == {"access_token": "test-token", "token_type": "bearer"}
