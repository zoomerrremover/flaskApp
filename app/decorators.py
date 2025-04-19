from http import HTTPStatus
from flask import requst, Response
from authentication import authenticate
from functools import wraps
from pydantic.main import BaseModel, ValidationError


def requires_auth(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not authenticate():
            return Response("Not authorized",HTTPStatus.FORBIDDEN)
        return f(*args, **kwargs)
    return decorated

def validate_request(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = model(**request.get_json())
                return f(data, *args, **kwargs)
            except ValidationError as e:
                return jsonify({"error": e.errors()}), HTTPStatus.BAD_REQUEST
        return wrapper
    return decorator

def serialize_response(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            if isinstance(result, model):
                return jsonify(result.model_dump())
            elif isinstance(result, tuple) and isinstance(result[0], model):
                return jsonify(result[0].model_dump()), *result[1:]
            return result
        return wrapper
    return decorator
