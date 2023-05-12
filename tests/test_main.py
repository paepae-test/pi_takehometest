import random
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import main_app


client = TestClient(main_app)


auth_headers = None

def get_auth_headers():
    global auth_headers

    if auth_headers is None:
        response = client.post(
            "/auth",
            json={
                "username": settings.TEST_APP_USER_USERNAME,
                "password": settings.TEST_APP_USER_PASSWORD,
            },
        )
        assert response.status_code == 200
        res_json = response.json()
        access_token = res_json["access_token"]
        auth_headers = {
            "Authorization": f"Bearer {access_token}",
        }
        print("auth_headers:", auth_headers)

    return auth_headers


def test_create_get_update_search_user():
    random_id = random.randint(1, 1000000000)
    name = f"test_{random_id}"
    email = f"test_{random_id}@test.com"

    response = client.post(
        "/users",
        json={
            "name": name,
            "email": email,
        },
        headers=get_auth_headers(),
    )
    assert response.status_code == 200
    res_json = response.json()
    user_id = res_json["id"]

    response = client.get(f"/users/{user_id}", headers=get_auth_headers())
    assert response.status_code == 200
    res_json = response.json()
    assert "id" in res_json and res_json["id"] == user_id
    assert "name" in res_json and res_json["name"] == name
    assert "email" in res_json and res_json["email"] == email

    response = client.get(f"/users?name={name}", headers=get_auth_headers())
    assert response.status_code == 200
    res_json = response.json()
    assert len(res_json) >= 1
    found = False
    for user in res_json:
        if "id" in user and user["id"] == user_id:
            assert "name" in user and user["name"] == name
            assert "email" in user and user["email"] == email
            found = True
            break
    assert found

    updated_name = f"{name}_updated"
    updated_email = f"{email}_updated"
    response = client.put(
        f"/users/{user_id}",
        json={
            "name": updated_name,
            "email": updated_email,
        },
        headers=get_auth_headers(),
    )
    assert response.status_code == 200
    res_json = response.json()
    assert "id" in res_json and res_json["id"] == user_id
    assert "name" in res_json and res_json["name"] == updated_name
    assert "email" in res_json and res_json["email"] == updated_email

    response = client.get(f"/users/{user_id}", headers=get_auth_headers())
    assert response.status_code == 200
    res_json = response.json()
    assert "id" in res_json and res_json["id"] == user_id
    assert "name" in res_json and res_json["name"] == updated_name
    assert "email" in res_json and res_json["email"] == updated_email


def test_get_user_401():
    response = client.get("/users/1")
    assert response.status_code == 401


def test_add_user_401():
    response = client.post(
        "/users",
        json={
            "name": "test",
            "email": "test",
        },
    )
    assert response.status_code == 401


def test_update_user_401():
    response = client.put(
        "/users/1",
        json={
            "name": "test",
            "email": "test",
        },
    )
    assert response.status_code == 401


def test_search_user_401():
    response = client.get("/users?name=test")
    assert response.status_code == 401


def test_search_user_empty_result():
    response = client.get("/users?name=test_not_existed", headers=get_auth_headers())
    assert response.status_code == 200
    res_json = response.json()
    assert len(res_json) == 0
