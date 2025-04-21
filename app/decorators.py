from http import HTTPStatus
from flask import request, Response, jsonify
from app.authentication import authenticate
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


def validate_request_params(*expected_params):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            missing_params = []
            for param_name in expected_params:
                if param_name not in request.args:
                    missing_params.append(param_name)

            if missing_params:
                missing_params_str = ", ".join(missing_params)
                error_message = f"Missing required parameters: {missing_params_str}"
                return Response(error_message, HTTPStatus.BAD_REQUEST)

            return func(*args, **kwargs)
        return wrapper
    return decorator


