from functools import wraps
from app.common import user_role_is_satisfactory
from app.constants import UserRolesEnum, CommonConstantsEnum, ErrorsMsgEnum
from app.db.service.user import get_user_by_id
from app.exceptions import AuthorizationError, AuthenticationError
from app.settings import AUTH_HEADER
from flask import request
from app.security.jwt_service import verify_jwt


def require_auth(role: UserRolesEnum = UserRolesEnum.user):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get(AUTH_HEADER)
            if auth_header and auth_header.startswith(CommonConstantsEnum.AUTH_PREFIX):
                token = auth_header.split(' ')[1]
                user_token = verify_jwt(token)
                user_db = get_user_by_id(user_token.id)
                if user_db and user_role_is_satisfactory(user_db.role, role):
                    g.current_user = user_db
                    return f(*args, **kwargs)
                else:
                    raise AuthorizationError(ErrorsMsgEnum.ERR_UNSATISFACTORY_ROLE)
            else:
                raise AuthenticationError(ErrorsMsgEnum.ERR_LOGIN_REQUIRED)
        return wrapper
    return decorator
