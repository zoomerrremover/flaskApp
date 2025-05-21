from werkzeug.exceptions import HTTPException
from http import HTTPStatus


class AuthorizationError(HTTPException):
    code = HTTPStatus.UNAUTHORIZED


class AuthenticationError(HTTPException):
    code = HTTPStatus.FORBIDDEN


class NothingFoundError(HTTPException):
    code = HTTPStatus.NO_CONTENT


class ConflictingDataError(HTTPException):
    code = HTTPStatus.CONFLICT


class InvalidDataError(HTTPException):
    code = HTTPStatus.BAD_REQUEST
