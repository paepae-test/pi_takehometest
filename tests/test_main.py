import random
from fastapi.testclient import TestClient

from app.main import main_app


client = TestClient(main_app)


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
    )
    assert response.status_code == 200
    res_json = response.json()
    user_id = res_json["id"]

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    res_json = response.json()
    assert "id" in res_json and res_json["id"] == user_id
    assert "name" in res_json and res_json["name"] == name
    assert "email" in res_json and res_json["email"] == email

    response = client.get(f"/users?name={name}")
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
    )
    assert response.status_code == 200
    res_json = response.json()
    assert "id" in res_json and res_json["id"] == user_id
    assert "name" in res_json and res_json["name"] == updated_name
    assert "email" in res_json and res_json["email"] == updated_email

    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    res_json = response.json()
    assert "id" in res_json and res_json["id"] == user_id
    assert "name" in res_json and res_json["name"] == updated_name
    assert "email" in res_json and res_json["email"] == updated_email
