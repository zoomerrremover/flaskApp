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


class UserRole(StrEnum):
    user = 'user'
    editor = 'editor'
    admin = 'admin'


class Errors(StrEnum):
    ERR_USERNAME_VALIDITY = "Username shall not contain any spaces, and shall be between 3 and 20 characters !"
    ERR_USERNAME_ORIGINAL = "Username shall be original."
    ERR_PASSWORD = "Password shall contain at least 1 letter."
    ERR_ROLES = "Role shall match existing role."
    ERR_TEXT_CONTENT = "Text content shall not be less than 3 characters."
    ERR_AUTH = "Username of password does not match"
    ERR_JWT = "JWT token does not match signature"
    ERR_UNSATISFACTORY_ROLE = "Your role is unsatisfactory to do that action."
    ERR_LOGIN_REQUIRED = "Login required"
    ERR_EMAIL_VALID = "The email is supposed to be valid"
    ERR_EMAIL_IS_ORIGINAL = "The email supposed to be original"


class Constants(StrEnum):
    AUTH_PREFIX = 'Bearer '
