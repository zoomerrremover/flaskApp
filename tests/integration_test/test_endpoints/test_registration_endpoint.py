def test_successful_registration(client, generate_users):
    user_data = next(generate_users())
    print(user_data)
    response = client.post("/registration/", json=user_data)
    assert response.status_code == 200
    response_json = response.json
    assert response_json is not None
    assert "access_token" in response_json
    assert (
        isinstance(response_json["access_token"], str)
        and len(response_json["access_token"]) > 0
    )


def test_registration_missing_username(client, generate_users):
    user_data = next(generate_users())
    payload = user_data.copy()
    del payload["username"]
    response = client.post("/registration/", json=payload)
    assert response.status_code == 400


def test_registration_missing_password(client, generate_users):
    user_data = next(generate_users())
    payload = user_data.copy()
    del payload["password"]
    response = client.post("/registration/", json=payload)
    assert response.status_code == 400


def test_registration_missing_email(client, generate_users):
    user_data = next(generate_users())
    payload = user_data.copy()
    del payload["email"]
    response = client.post("/registration/", json=payload)
    assert response.status_code == 400


def test_registration_invalid_email_format(client, generate_users):
    user_data = next(generate_users())
    payload = user_data.copy()
    payload["email"] = "invalid-email"
    response = client.post("/registration/", json=payload)
    assert response.status_code == 400


def test_registration_invalid_password_format(client, generate_users):
    user_data = next(generate_users())
    payload = user_data.copy()
    payload["password"] = "short"
    response = client.post("/registration/", json=payload)
    assert response.status_code == 400


def test_double_registration(client, generate_users):
    user_data = next(generate_users())
    response1 = client.post("/registration/", json=user_data)
    assert response1.status_code == 200
    assert "access_token" in response1.json
    response2 = client.post("/registration/", json=user_data)
    assert response2.status_code in [400, 409]


def test_registration_empty_payload(client):
    response = client.post("/registration/", json={})
    assert response.status_code == 400


def test_registration_invalid_json_format(client):
    response = client.post(
        "/registration/",
        data="this is not json",
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code in [
        400,
        415,
    ]


def test_registration_with_extra_fields(client, generate_users):
    user_data = next(generate_users())
    payload = user_data.copy()
    payload["extra_field"] = "some_value"
    payload["another_unexpected_key"] = 123
    response = client.post("/registration/", json=payload)
    assert response.status_code in [200, 400]


def test_registration_username_with_spaces(client, generate_users):
    user_data = next(generate_users())
    payload = user_data.copy()

    payload["username"] = f"   {user_data['username']}   "
    response = client.post("/registration/", json=payload)
    assert response.status_code in [200, 400]


def test_registration_email_with_spaces(client, generate_users):
    user_data = next(generate_users())
    payload = user_data.copy()

    payload["email"] = f"   {user_data['email']}   "
    response = client.post("/registration/", json=payload)
    assert response.status_code in [200, 400]

