from fuzzywuzzy import fuzz
from app.constants import UserRole
from http import HTTPStatus
from flask import jsonify, Response

def str_compare(base_string: str ,string_to_compare: str, index: int) -> bool:
    return fuzz.ratio(base_string, string_to_compare) > index

def user_role_is_satisfactory(role_input: UserRole, role_required: UserRole) -> bool:
    if role_input == UserRole.admin:
        return True
    elif role_input == UserRole.editor:
        return role_required == UserRole.editor or role_required == UserRole.user
    else:
        return role_required == UserRole.user
