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
    ERROR_USERNAME_VALIDITY = "Username shall not contain any spaces, and shall be between 3 and 20 characters !"
    ERROR_USERNAME_ORIGINAL = "Username shall be original."
    ERROR_PASSWORD = "Password shall contain at least 1 letter."
    ERROR_ROLES = "Role shall match existing role."
    ERROR_TEXT_CONTENT = "Text content shall not be less than 3 characters."
    ERROR_AUTH = "Username of password does not match"
    ERROR_JWT = "JWT token does not match signature"
    ERROR_FIELD_MISSING = ""
    ERROR_UNSATISFACTORY_ROLE = "Your role is unsatisfactory to do that action."
    ERROR_LOGIN_REQUIRED = "Login required"
    ERROR_EMAIL_VALID = "The email is supposed to be valid"
    ERROR_EMAIL_IS_ORIGINAL = "The email supposed to be original"
    ERROR_COURSE_UPDATE_CREATE = ""
    ERROR_ARTICLE_UPDATE_CREATE = ""
    ERROR_SUGGESTION_UPDATE_CREATE = ""
    ERROR_USER_UPDATE = ""
    ERROR_DELETE = ""
    ERROR_LIMIT = ""
    ERROR_USER_DOES_NOT_EXIST = "User does not exist"


class CommonConstantsEnum(StrEnum):
    AUTH_PREFIX = "Bearer "
