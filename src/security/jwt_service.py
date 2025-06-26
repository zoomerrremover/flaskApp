import jwt
from datetime import datetime, timedelta, timezone
from flask import jsonify
from src.settings import JWT_KEY, ACCESS_TOKEN_TIME
from src.db import User
from src.exceptions import AuthenticationError
from src.constants import ErrorsMsgEnum, AuthConstantsEnum


def generate_jwt(user: User):
    time_now = datetime.now(timezone.utc)
    payload = {
        "user_id": user.id,
        "exp": (time_now + timedelta(minutes=ACCESS_TOKEN_TIME)).timestamp(),
        "iat": time_now.timestamp(),
    }
    return jwt.encode(payload, JWT_KEY, AuthConstantsEnum.ALGORITHM)


def generate_json_jwt(user: User):
    jwt_token = generate_jwt(user)
    return jsonify(
        {
            "access_token": jwt_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_TIME * 60,
        }
    )


def verify_jwt(token):
    try:
        payload = jwt.decode(
            token,
            JWT_KEY,
            algorithms=[AuthConstantsEnum.ALGORITHM]
        )
        result = User(id=payload["user_id"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise AuthenticationError(ErrorsMsgEnum.ERROR_JWT_INVALID)
    return result
