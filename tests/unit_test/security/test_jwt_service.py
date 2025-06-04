from src.security.jwt_service import generate_jwt, verify_jwt, generate_json_jwt
from datetime import datetime, timedelta
from flask import Response
import json


def test_generate_jwt_payload_and_encoding(
    real_user_instance, fixed_datetime, mock_jwt_encode
):
    """
    Tests that generate_jwt creates the correct payload and calls jwt.encode.
    Uses a real User model instance.
    """
    user_id = real_user_instance.id
    expected_iat = fixed_datetime.timestamp()
    expected_exp = (
        fixed_datetime + timedelta(minutes=15)
    ).timestamp()  # MOCK_ACCESS_TOKEN_TIME is 15

    token = generate_jwt(real_user_instance)

    # Assert jwt.encode was called exactly once
    mock_jwt_encode.assert_called_once()

    # Get the arguments passed to jwt.encode
    args, kwargs = mock_jwt_encode.call_args

    # Assert the payload is correct
    assert "user_id" in args[0]
    assert args[0]["user_id"] == user_id
    assert "exp" in args[0]
    # Allow for slight floating point differences if comparing timestamps directly
    assert abs(args[0]["exp"] - expected_exp) < 0.01
    assert "iat" in args[0]
    assert abs(args[0]["iat"] - expected_iat) < 0.01

    # Assert encoding parameters are correct
    print(args)
    # assert kwargs["key"] == "test_secret_key_from_fixture"
    # assert kwargs["algorithm"] == "HS256"
    # Assert the function returns the mocked token string
    assert token == "mock_jwt_token_string"


def test_generate_json_jwt_structure(real_user_instance, mock_jwt_encode, app):
    """
    Tests that generate_json_jwt returns a valid Flask JSON Response
    with the correct structure and headers.
    Uses a real User model instance.
    """
    with app.app_context():
        flask_response = generate_json_jwt(real_user_instance)

    # 1. Assert it's a Flask Response object
    assert isinstance(flask_response, Response)

    # 2. Assert the Content-Type header is application/json
    assert flask_response.headers["Content-Type"] == "application/json"

    # 3. Extract the JSON data from the response body
    # flask_response.data contains the response body as bytes
    # .decode('utf-8') converts it to a string
    # json.loads() parses the string into a Python dict
    try:
        parsed_json = json.loads(flask_response.data.decode("utf-8"))
    except json.JSONDecodeError:
        pytest.fail("Flask response body is not valid JSON")

    # 4. Assert the structure and content of the parsed JSON
    assert "access_token" in parsed_json
    assert (
        parsed_json["access_token"] == "mock_jwt_token_string"
    )  # Assumes your mock_jwt_encode returns this
    assert "token_type" in parsed_json
    assert parsed_json["token_type"] == "bearer"

    # 5. Ensure generate_jwt (or whatever internal function `mock_jwt_encode` replaces)
    #    was called internally.
    mock_jwt_encode.assert_called_once()  # generate_json_jwt calls generate_jwt, which calls jwt.encode
