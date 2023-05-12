from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import main_app


client = TestClient(main_app)


def test_auth_success():
    response = client.post(
        "/auth",
        json={
            "username": settings.TEST_APP_USER_USERNAME,
            "password": settings.TEST_APP_USER_PASSWORD,
        },
    )
    assert response.status_code == 200
    res_json = response.json()
    assert "access_token" in res_json and res_json["access_token"]
    assert "token_type" in res_json and res_json["token_type"] == "bearer"


def test_auth_fail():
    response = client.post(
        "/auth",
        json={
            "username": settings.TEST_APP_USER_USERNAME,
            "password": settings.TEST_APP_USER_PASSWORD + "wrong_password",
        },
    )
    assert response.status_code == 401
