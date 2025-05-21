from app.settings import JWT_KEY, ALGORITHM, ACCESS_TOKEN_TIME
from app.db.models.concrete import User
from datetime import datetime, timedelta
import jwt
from flask import jsonify
from app.exceptions import AuthenticationError
from app.constants import ErrorsMsgEnum


def generate_jwt(user: User):
    payload = \
    {
        'user_id': user.id,
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TIME),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_KEY, ALGORITHM)


def generate_json_jwt(user: User):
    jwt_token = generate_jwt(user)
    return jsonify({'access_token': jwt_token, 'token_type': 'jwt', 'expires_in': ACCESS_TOKEN_TIME * 60})


def verify_jwt(token):
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        result = User(id=payload['user_id'])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        raise AuthenticationError(ErrorsMsgEnum.ERR_JWT)
    return result
