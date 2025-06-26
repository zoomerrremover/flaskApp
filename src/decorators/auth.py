from functools import wraps
from flask import request, g
from src.common import user_role_is_satisfactory
from src.constants import UserRolesEnum, AuthConstantsEnum, ErrorsMsgEnum
from src.db import User
from src.exceptions import AuthorizationError, AuthenticationError
from src.security import verify_jwt


def require_auth(role: UserRolesEnum = UserRolesEnum.USER):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get(AuthConstantsEnum.AUTH_HEADER)
            if not auth_header or not auth_header.startswith(
                AuthConstantsEnum.AUTH_PREFIX
            ):
                raise AuthenticationError(ErrorsMsgEnum.ERROR_FIELD_REQUIRED)
            token = auth_header.split(" ")[1]
            user_token = verify_jwt(token)
            user_db = User.get_by_id(user_token.id)
            if not user_db:
                raise AuthenticationError(ErrorsMsgEnum.ERROR_FIELD_REQUIRED)
            if not user_role_is_satisfactory(user_db.role, role):
                raise AuthorizationError(ErrorsMsgEnum.ERROR_UNAUTHORIZED_ROLE)
            g.current_user = user_db
            return f(*args, **kwargs)

        return wrapper

    return decorator
