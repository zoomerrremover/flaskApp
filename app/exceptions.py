from http import HTTPStatus

class AuthorizationError(Exception):
    code = HTTPStatus.UNAUTHORIZED


class AuthenticationError(Exception):
    code = HTTPStatus.FORBIDDEN


class ConflictingDataError(Exception):
    code = HTTPStatus.CONFLICT


class InvalidDataError(Exception):
    code = HTTPStatus.BAD_REQUEST
