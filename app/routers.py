from flask import Flask
from app.endpoints.posts import post_route
from app.endpoints.user import user_route
from app.endpoints.registration import auth_route

def add_routes(app: Flask):
    app.register_blueprint(user_route)
    app.register_blueprint(auth_route)