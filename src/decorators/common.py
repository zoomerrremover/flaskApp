from flask import request, Response, jsonify, g
from functools import wraps
from pydantic.main import BaseModel
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import IntegrityError
from src.exceptions import InvalidDataError
from src.db import session
from src.constants import ErrorsMsgEnum
from typing import List, Tuple


def validate_model_request(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = model(**request.get_json())
                return f(data, *args, **kwargs)
            except ValueError as e:
                problematic_fields: List[Tuple[str, ...]] = []
                for error_detail in e.errors():
                    field_location = error_detail.get('loc')
                    if field_location:
                        problematic_fields.append(field_location)
                raise InvalidDataError(f"{ErrorsMsgEnum.ERROR_FIELD_REQUIRED}{problematic_fields}")


        return wrapper

    return decorator


def validate_model_params(model: type[BaseModel]):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                data = model(**request.args)
                return f(data, *args, **kwargs)
            except ValueError as e:
                problematic_fields: List[Tuple[str, ...]] = []
                for error_detail in e.errors():
                    field_location = error_detail.get('loc')
                    if field_location:
                        problematic_fields.append(field_location)
                raise InvalidDataError(f"{ErrorsMsgEnum.ERROR_FIELD_REQUIRED}{problematic_fields}")

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
