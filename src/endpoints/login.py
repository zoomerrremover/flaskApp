from flask import Blueprint, render_template, abort, Response, jsonify
from ..decorators import validate_model_params
from ..db import User
from ..security import generate_json_jwt, verify_password
from ..models import UserLogInModel

login_route = Blueprint("login_route", __name__, url_prefix="/login")
from ..decorators import (
    validate_model_request,
    validate_model_params,
    handle_exception,
)


@login_route.route("/", methods=["POST"])
@validate_model_params(UserLogInModel)
def route_login(model: UserLogInModel):
    user = User.get_user_by_name(model.username)
    if user and verify_password(model.password, user.password):
        return generate_json_jwt(user)
    else:
        raise AuthenticationError(ErrorsMsgEnum.ERR_AUTH)
