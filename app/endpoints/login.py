from flask import Blueprint, render_template, abort, Response, jsonify
from app.decorators import validate_model_params
from app.db.service.user_service import get_user_login
from app.security.security import generate_json_jwt
from app.models.user import UserLogInModel

login_route = Blueprint('login_route', __name__, url_prefix='/login')


@login_route.route("/", methods=['POST'])
@validate_model_params(UserLogInModel)
def route_login(model: UserLogInModel):
    user = get_user_login(model.username, model.password)
    return generate_json_jwt(user)
