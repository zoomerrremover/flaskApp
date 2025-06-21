from http import HTTPStatus
from src.security import generate_json_jwt
from src.db import User
from urllib.parse import urlencode


def test_get_user_successful(client, registered_user):

    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/user/", headers=headers)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json is not None
    assert response_json["username"] == user_data["username"]
    assert response_json["role"] == "user"
    assert response_json["id"] is not None


def test_get_user_unauthorized_no_token(client):
    response = client.get("/user/")
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_user_unauthorized_invalid_token(client):
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get("/user/", headers=headers)
    assert response.status_code == HTTPStatus.FORBIDDEN


# PATCH /user/
def test_update_user_successful_all_fields(
    client, registered_user, generate_users
):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    generated_user_data = next(generate_users())
    new_username = generated_user_data["username"]
    new_email = generated_user_data["email"]
    new_password = generated_user_data["password"]
    update_data = urlencode({
        "username": new_username,
        "email": new_email,
        "password": new_password
    })
    response = client.patch(f"/user/?{update_data}/", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""
    get_response = client.get("/user/", headers=headers)
    assert get_response.status_code == HTTPStatus.OK
    response_json = get_response.json
    assert response_json["username"] == new_username


def test_update_user_unauthorized(client, generate_users):
    update_data = {"username": "new_username"}
    response = client.patch(f"/user/?{update_data}/")
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_user_invalid_data_email_format(generate_users,
                                               client,
                                               registered_user):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    generated_user_data = next(generate_users())
    new_username = generated_user_data["username"]
    new_password = generated_user_data["password"]
    update_data = urlencode({
        "username": new_username,
        "email": "invalid_email",
        "password": new_password
    })
    response = client.patch(f"/user/?{update_data}/", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user_invalid_data_password_format(generate_users, client, registered_user):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    generated_user_data = next(generate_users())
    new_username = generated_user_data["username"]
    new_email = generated_user_data["email"]
    update_data = urlencode({
        "username": new_username,
        "email": new_email,
        "password": "short"
    })
    response = client.patch(f"/user/?{update_data}/", headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user_email_already_exists(
    client, registered_user, generate_users
):
    user_gen = registered_user("user", 2)
    user1_data = next(user_gen)
    user2_data = next(user_gen)
    user1_token = user1_data["access_token"]
    headers = {"authorization": f"Bearer {user1_token}"}
    update_data = urlencode({
        "username": user1_data["username"],
        "email": user2_data["email"],
        "password": user1_data["password"]
    })
    response = client.patch(f"/user/?{update_data}/", headers=headers)
    assert response.status_code in [HTTPStatus.CONFLICT, HTTPStatus.BAD_REQUEST]


def test_update_user_no_payload(client, registered_user):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.patch("/user/", json={}, headers=headers)
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.BAD_REQUEST]


def test_update_user_extra_fields(client, registered_user, generate_users):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = urlencode({
        "username": user_data["username"],
        "email": user_data["email"],
        "password": user_data["password"],
        "id": 233,
        "date": "June 15 2022",
        "role": "admin"

    })
    response = client.patch(f"/user/?{update_data}/", headers=headers)
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.BAD_REQUEST]


# DELETE /user/
def test_delete_user_successful(client, registered_user):
    user_data = next(registered_user())
    access_token = user_data["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete("/user/", headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.data == b""
    get_response = client.get("/user/", headers=headers)
    assert (
        get_response.status_code == HTTPStatus.FORBIDDEN
    )


def test_delete_user_unauthorized(client):
    response = client.delete("/user/")
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user_non_existent_token(client, app):
    with app.app_context():
        non_existent_user_id = User(id=9999999)
        invalid_token = generate_json_jwt(non_existent_user_id)
        headers = {"Authorization": f"Bearer {invalid_token}"}
        response = client.delete("/user/", headers=headers)
        assert response.status_code == HTTPStatus.FORBIDDEN

