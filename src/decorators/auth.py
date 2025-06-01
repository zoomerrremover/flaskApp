from functools import wraps
from flask import request, g
from ..common import user_role_is_satisfactory
from ..constants import UserRolesEnum, CommonConstantsEnum, ErrorsMsgEnum
from ..db import User
from ..exceptions import AuthorizationError, AuthenticationError
from ..settings import AUTH_HEADER
from ..security import verify_jwt


def require_auth(role: UserRolesEnum = UserRolesEnum.user):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get(AUTH_HEADER)
            if not auth_header or not auth_header.startswith(CommonConstantsEnum.AUTH_PREFIX):
                raise AuthenticationError(ErrorsMsgEnum.ERROR_LOGIN_REQUIRED)
            token = auth_header.split(" ")[1]
            user_token = verify_jwt(token)
            user_db = User.get_by_id(user_token.id)
            if not user_db:
                raise AuthorizationError(ErrorsMsgEnum.ERROR_USER_DOES_NOT_EXIST)
            if not user_role_is_satisfactory(user_db.role, role):
                raise AuthorizationErrorAuthorizationError(ErrorsMsgEnum.ERROR_UNSATISFACTORY_ROLE)
            g.current_user = user_db
            return f(*args, **kwargs)

        return wrapper

    return decorator
