from flask import request, Response, jsonify, g
from functools import wraps
from pydantic.main import BaseModel
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from ..exceptions import InvalidDataError
from ..db import session
from ..constants import ErrorsMsgEnum


def validate_model_request(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = model(**request.get_json())
            except ValueError:
                raise InvalidDataError(ErrorsMsgEnum.ERROR_FIELD_MISSING)
            return f(data, *args, **kwargs)

        return wrapper

    return decorator


def validate_model_params(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = model(**request.args)
            except ValueError:
                raise InvalidDataError(ErrorsMsgEnum.ERROR_FIELD_MISSING)
            return f(data, *args, **kwargs)

        return wrapper

    return decorator


def handle_db_exception(catch_exception: Exception, http_exception: HTTPException):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except catch_exception as e:
                session.rollback()
                print(e)
                raise http_exception

        return wrapper

    return decorator
