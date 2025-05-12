from flask import request, Response, jsonify
from functools import wraps
from pydantic.main import BaseModel
from app.security.security import verify_jwt
from app.settings import AUTH_HEADER, AUTH_PREFIX
from app.exceptions import ConflictingDataError, AuthenticationError, AuthorizationError
from app.constants import Errors, UserRole
from app.common import user_role_is_satisfactory
from app.db.service.user_service import get_user_by_id

def require_auth(role:UserRole = UserRole.user):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get(AUTH_HEADER)
            if auth_header and auth_header.startswith(AUTH_PREFIX):
                token = auth_header.split(' ')[1]
                user = verify_jwt(token)
                if get_user_by_id(user.id) and user_role_is_satisfactory(user.role, role):
                    request.current_user = user
                    return f(*args,**kwargs)
                else:
                    raise AuthorizationError(Errors.ERR_UNSATISFACTORY_ROLE)
            else:
                raise AuthenticationError(Errors.ERR_LOGIN_REQUIRED)
        return wrapper
    return decorator


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
