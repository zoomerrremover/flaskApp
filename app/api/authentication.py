from http import HTTPStatus
from flask import Flask, request, Response

users = {
    "admin": 123,
    "guest": 456
}

def authenticate():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return False
    user = users.get(auth.username)
    if not user or user != auth.password:
        return False
    return auth.username, auth.password

def requires_auth(f):
    """Decorator to enforce HTTP basic auth."""
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not authenticate():
            return Response("Not authorized",HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)
    return decorated
