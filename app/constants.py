from enum import Enum

class UserRole(Enum):
    user = 'user'
    editor = 'editor'
    admin = 'admin'

    @staticmethod
    def compare(role_received, role_required) -> bool:
        match role_required:
            case UserRole.admin:
                if role_received == UserRole.admin:
                    result = True
                else:
                    result = False

            case UserRole.editor:
                if (role_received == UserRole.editor or
                        role_received == UserRole.admin) :
                    result = True
                else:
                    result = False

            case UserRole.user:
                if (role_received == UserRole.user or
                    role_received == UserRole.editor or
                    role_received == UserRole.admin) :
                    result = True
                else:
                    result = False

            case _:
                result = False
        return result


class Errors:
    ERR_USERNAME_VALIDITY = "Username shall not contain any spaces, and shall be between 3 and 20 characters !"
    ERR_USERNAME_ORIGINAL = "Username shall be original."
    ERR_PASSWORD = "Password shall contain at least 1 letter."
    ERR_ROLES = "Role shall match existing role."
    ERR_TEXT_CONTENT = "Text content shall not be less than 3 characters."
    ERR_AUTH = "Username of password does not match"
    ERR_LOGIN_REQUIRED = "Login required"
    ERR_EMAIL_VALID = "The email is supposed to be valid"
    ERR_EMAIL_IS_ORIGINAL = "The email supposed to be original"
