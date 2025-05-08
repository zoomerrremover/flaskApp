from flask import Flask
from app.endpoints.user import user_route
from app.endpoints.registration import registration_route
from app.endpoints.login import login_route
from app.endpoints.article import article_route

def add_routes(app: Flask):
    app.register_blueprint(user_route)
    app.register_blueprint(registration_route)
    app.register_blueprint(login_route)
    app.register_blueprint(article_route)
