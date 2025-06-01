from flask import request, Response, jsonify, g
from functools import wraps
from pydantic.main import BaseModel
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError


def validate_model_request(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = model(**request.get_json())
            return f(data, *args, **kwargs)

        return wrapper

    return decorator


def validate_model_params(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = model(**request.args)
            return f(data, *args, **kwargs)

        return wrapper

    return decorator


def handle_exception(catch_exception: Exception, http_exception: HTTPException):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except catch_exception:
                raise http_exception

        return wrapper

    return decorator
