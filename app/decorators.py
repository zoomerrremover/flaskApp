from flask import requst, Response
from authentication import authenticate

def requires_auth(f):
    from functools import wraps

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not authenticate():
            return Response("Not authorized",HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)
    return decorated

