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
                raise InvalidDataError(ErrorsMsgEnum.ERROR_FIELD_REQUIRED)
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
                raise InvalidDataError(ErrorsMsgEnum.ERROR_FIELD_REQUIRED)
            return f(data, *args, **kwargs)

        return wrapper

    return decorator


def handle_db_exception(message: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except IntegrityError as e:
                session.rollback()
                print(e)
                raise InvalidDataError(message)

        return wrapper

    return decorator
