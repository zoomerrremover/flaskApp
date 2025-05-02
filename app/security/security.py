from app.settings import JWT_KEY, ALGORITHM, ACCESS_TOKEN_TIME
from app.db.models import User
from datetime import datetime, timedelta
import jwt
from flask import jsonify

def generate_jwt(user: User):
    payload = {
        'user_id': user.id,
        'username': user.username,
        'role': user.role,
        'exp': datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_TIME),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_KEY, ALGORITHM)


def generate_json_jwt(user: User):
    jwttoken = generate_jwt(user)
    return jsonify({'access_token': jwttoken ,'token_type': 'jwt', 'expires_in': ACCESS_TOKEN_TIME*60 })


def verify_jwt(token):
    try:
        payload = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        return User(id=payload['user_id'], username=payload['username'],
                    role=payload['role'])
    except [jwt.ExpiredSignatureError, jwt.InvalidTokenError]:
        return None
