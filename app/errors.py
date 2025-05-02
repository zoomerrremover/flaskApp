from http import HTTPStatus

class AuthorizationError(Exception):
    code = HTTPStatus.UNAUTHORIZED

class AuthenticationError(Exception):
    code = HTTPStatus.FORBIDDEN

class ConflictingData(Exception):
    code = HTTPStatus.CONFLICT
