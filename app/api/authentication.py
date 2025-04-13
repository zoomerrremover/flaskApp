from http import HTTPStatus
from flask import Flask, request, Response

def authenticate():
#   auth = request.authorization
#   if not auth or not auth.username or not auth.password:
#       return False
#   user = users.get(auth.username)
#   if not user or user != auth.password:
#        return False
#    return auth.username, auth.password
    return True

def requires_auth(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not authenticate():
            return Response("Not authorized",HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)
    return decorated
