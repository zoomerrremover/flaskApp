import jwt
from datetime import datetime, timedelta, timezone
from flask import jsonify
from ..settings import JWT_KEY, ALGORITHM, ACCESS_TOKEN_TIME
from ..db import User
from ..exceptions import AuthenticationError
from ..constants import ErrorsMsgEnum


def generate_jwt(user: User):
    now = datetime.now(timezone.utc)
    payload = {
        "user_id": user.id,
        "exp": (now + timedelta(minutes=ACCESS_TOKEN_TIME)).timestamp(),
        "iat": now.timestamp(),
    }
    return jwt.encode(payload, JWT_KEY, ALGORITHM)


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
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        result = User(id=payload["user_id"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise AuthenticationError(ErrorsMsgEnum.ERROR_JWT_INVALID)
    return result
