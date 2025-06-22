import pytest
from http import HTTPStatus
from urllib.parse import urlencode


def test_login_successful(client, registered_user):
    user_data = next(registered_user())
    login_payload = {
        "username": user_data["username"],
        "password": user_data["password"],
    }
    response = client.post(f"/login/?{urlencode(login_payload)}")
    print(f"Response error login : {response.text}")
    assert response.status_code == HTTPStatus.OK
    response_json = response.json
    assert response_json is not None
    assert "access_token" in response_json
    assert isinstance(response_json["access_token"], str)
    assert len(response_json["access_token"]) > 0


def test_login_incorrect_password(client, registered_user):
    user_data = next(registered_user())
    
    login_payload = {
        "username": user_data["username"],
        "password": "wrong_password_123!"
    }
    
    response = client.post(f"/login/?{urlencode(login_payload)}")
    
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_non_existent_username(client, generate_users):
    fake_user_data = next(generate_users()) 
    
    login_payload = {
        "username": fake_user_data["username"],
        "password": fake_user_data["password"]
    }
    
    response = client.post(f"/login/?{urlencode(login_payload)}")
    
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_login_missing_username(client, registered_user):
    user_data = next(registered_user())
    
    login_payload = {
        "password": user_data["password"]
    }
    
    response = client.post(f"/login/?{urlencode(login_payload)}")
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "username" in response.text


def test_login_missing_password(client, registered_user):
    user_data = next(registered_user())
    
    login_payload = {
        "username": user_data["username"],
    }
    
    response = client.post(f"/login/?{urlencode(login_payload)}")
    
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "password" in response.text


def test_login_empty_payload(client):
    login_payload = {} # Empty payload, will result in missing username/password
    response = client.post(f"/login/?{urlencode(login_payload)}")
    
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_invalid_username_type(client, registered_user):
    user_data = next(registered_user())
    
    login_payload = {
        "username": 12345,
        "password": user_data["password"]
    }
    
    response = client.post(f"/login/?{urlencode(login_payload)}")
    
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_invalid_password_type(client, registered_user):
    user_data = next(registered_user())
    
    login_payload = {
        "username": user_data["username"],
        "password": ["a", "b", "c"]
    }
    
    response = client.post(f"/login/?{urlencode(login_payload)}")
    
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_extra_fields_in_payload(client, registered_user):
    user_data = next(registered_user())
    
    login_payload = {
        "username": user_data["username"],
        "password": user_data["password"],
        "extra_field": "some_value",
        "another_field": 123
    }
    
    response = client.post(f"/login/?{urlencode(login_payload)}")
    
    assert response.status_code == HTTPStatus.OK 
    assert "access_token" in response.json

