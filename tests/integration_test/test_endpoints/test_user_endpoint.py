from http import HTTPStatus
import jwt


def test_get_user_successful(client, registered_user_and_token):

    access_token, user_data = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/user/", headers=headers)
    assert response.status_code == HTTPStatus.OK
    response_json = response.data
    print(response_json)
    assert response_json is not None
    assert response_json["id"] == user_id
    assert response_json["username"] == user_data["username"]
    assert response_json["email"] == user_data["email"]


def test_get_user_unauthorized_no_token(client):
    response = client.get("/user/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_get_user_unauthorized_invalid_token(client):
    headers = {"Authorization": "Bearer invalid.token.here"}
    response = client.get("/user/", headers=headers)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


# PATCH /user/
def test_update_user_successful_username(
    client, registered_user_and_token, generate_users
):
    user_id, access_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    new_username = next(generate_users())["username"]  # Get a new unique username
    update_data = {"username": new_username}
    response = client.patch("/user/", json=update_data, headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.data == b""  # Expecting an empty response for successful update

    # Verify the update by fetching the user again
    get_response = client.get("/user/", headers=headers)
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["username"] == new_username


def test_update_user_successful_email(
    client, registered_user_and_token, generate_users
):
    user_id, access_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    new_email = next(generate_users())["email"]  # Get a new unique email
    update_data = {"email": new_email}
    response = client.patch("/user/", json=update_data, headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Verify the update
    get_response = client.get("/user/", headers=headers)
    assert get_response.status_code == HTTPStatus.OK
    assert get_response.json["email"] == new_email


def test_update_user_successful_password(
    client, registered_user_and_token, generate_users
):
    user_id, access_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}

    new_password = next(generate_users())["password"]  # Get a new strong password
    update_data = {"password": new_password}
    response = client.patch("/user/", json=update_data, headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Note: You generally cannot directly verify password updates by fetching,
    # as passwords are (and should be) hashed. You might need a separate login
    # endpoint to test if the new password works. For this test, we assume the
    # 200 OK means the update was processed by the backend.


def test_update_user_unauthorized(client, generate_users):
    update_data = {"username": "new_username"}
    response = client.patch("/user/", json=update_data)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_user_invalid_data_email_format(client, registered_user_and_token):
    _, access_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"email": "invalid-email"}
    response = client.patch("/user/", json=update_data, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user_invalid_data_password_format(client, registered_user_and_token):
    _, access_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {"password": "short"}  # Assuming 'short' is invalid
    response = client.patch("/user/", json=update_data, headers=headers)
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_update_user_username_already_exists(
    client, registered_user_and_token, generate_users
):
    # Register a second user to create a conflicting username
    _, _, user2_data = registered_user_and_token
    user1_id, user1_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {user1_token}"}

    # Attempt to change user1's username to user2's username
    update_data = {"username": user2_data["username"]}
    response = client.patch("/user/", json=update_data, headers=headers)

    # Expecting a conflict (409) or bad request (400) if username is unique
    assert response.status_code in [HTTPStatus.CONFLICT, HTTPStatus.BAD_REQUEST]


def test_update_user_email_already_exists(
    client, registered_user_and_token, generate_users
):
    # Register a second user to create a conflicting email
    _, _, user2_data = registered_user_and_token
    user1_id, user1_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {user1_token}"}

    # Attempt to change user1's email to user2's email
    update_data = {"email": user2_data["email"]}
    response = client.patch("/user/", json=update_data, headers=headers)

    # Expecting a conflict (409) or bad request (400) if email is unique
    assert response.status_code in [HTTPStatus.CONFLICT, HTTPStatus.BAD_REQUEST]


def test_update_user_no_payload(client, registered_user_and_token):
    _, access_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.patch("/user/", json={}, headers=headers)
    # Depending on validation, empty payload might be 200 (no change) or 400 (requires fields)
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.BAD_REQUEST]


def test_update_user_extra_fields(client, registered_user_and_token, generate_users):
    _, access_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    update_data = {
        "username": next(generate_users())["username"],
        "extra_field": "value",
    }
    response = client.patch("/user/", json=update_data, headers=headers)
    # Depending on your API's strictness, this could be 200 (ignores extra) or 400 (rejects extra)
    assert response.status_code in [HTTPStatus.OK, HTTPStatus.BAD_REQUEST]


# DELETE /user/
def test_delete_user_successful(client, registered_user_and_token):
    user_id, access_token, _ = registered_user_and_token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete("/user/", headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.data == b""

    # Verify the user is deleted by trying to fetch them
    get_response = client.get("/user/", headers=headers)
    assert (
        get_response.status_code == HTTPStatus.UNAUTHORIZED
    )  # User no longer exists or token invalid


def test_delete_user_unauthorized(client):
    response = client.delete("/user/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user_non_existent_token(client):
    # Create a token for a user ID that doesn't exist (e.g., deleted)
    non_existent_user_id = 9999999
    invalid_token = generate_access_token(non_existent_user_id)
    headers = {"Authorization": f"Bearer {invalid_token}"}
    response = client.delete("/user/", headers=headers)
    # Expecting 401 if the token is valid but the user ID doesn't map to a user
    # or 404 if your require_auth specifically checks for user existence.
    assert response.status_code == HTTPStatus.UNAUTHORIZED
