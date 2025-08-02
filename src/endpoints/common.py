from flask import Blueprint

from src.settings import APP_VERSION

common_route = Blueprint("common_route", __name__)


@common_route.route("/about", methods=["GET"])
def about():
    return APP_VERSION, 200
