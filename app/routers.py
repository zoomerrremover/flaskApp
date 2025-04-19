from flask import Flask
from app.end_points.posts import post_route
from app.end_points.user import user_route
from app.end_points.registration import registration_route

def add_routes(app: Flask):
    app.register_blueprint(post_route, url_prefix='/post')
    app.register_blueprint(user_route, url_prefix='/user')
    app.register_blueprint(registration_route, url_prefix='/register')