from enum import Enum


class StrEnum(str, Enum):
    """Create a string enum.

    Members of this class can be compared with strings, as well as members
    of other string enums, using the ==, !=, in, and not in operators.
    """

    def __new__(cls, *args, **kwds):
        if len(args) > 0:
            value = args[0]
            if not isinstance(value, str):
                raise TypeError(
                    f"Values of {cls.__name__} must be strings: "
                    f"{value!r} is not a string"
                )
        return super().__new__(cls, *args, **kwds)

    def __str__(self):
        return str(self.value)


class UserRolesEnum(StrEnum):
    user = "user"
    editor = "editor"
    admin = "admin"


class ErrorsMsgEnum(StrEnum):
    ERROR_USERNAME_INVALID = "Username must be 3-20 characters, without spaces."
    ERROR_USERNAME_NOT_ORIGINAL = "Username already exists."
    ERROR_PASSWORD_WEAK = "Password must contain at least one letter."
    ERROR_ROLE_INVALID = "Invalid role."
    ERROR_TEXT_TOO_SHORT = "Text must be at least 3 characters."
    ERROR_AUTH_FAILED = "Invalid username or password."
    ERROR_JWT_INVALID = "Invalid JWT signature."
    ERROR_FIELD_REQUIRED = "This field is required."
    ERROR_UNAUTHORIZED_ROLE = "Insufficient privileges for this action."
    ERROR_AUTHENTICATION_REQUIRED = "Authentication required."
    ERROR_EMAIL_INVALID = "Invalid email format."
    ERROR_EMAIL_EXISTS = "Email already exists."
    ERROR_COURSE_UPDATE_FAILED = "Failed to update/create course."
    ERROR_ARTICLE_UPDATE_FAILED = "Failed to update/create article."
    ERROR_SUGGESTION_UPDATE_FAILED = "Failed to update/create suggestion."
    ERROR_USER_UPDATE_FAILED = "Failed to update user."
    ERROR_DELETE_FAILED = "Failed to delete resource."
    ERROR_RATE_LIMITED = "Rate limit exceeded."
    ERROR_USER_NOT_FOUND = "User does not exist."
    ERROR_TEXT_CONTENT = "Text content is invalid"


class CommonConstantsEnum(StrEnum):
    AUTH_PREFIX = "Bearer "
