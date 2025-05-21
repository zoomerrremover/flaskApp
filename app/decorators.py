from flask import request, Response, jsonify, g
from functools import wraps
from pydantic.main import BaseModel
from app.security.security import verify_jwt
from flask import HTTPException
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


def exception_to_http(catch_exception: Exception, http_exception: HTTPException):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except catch_exception as e:
                raise http_exception(f"{e}")
        return wrapper
    return decorator
