from flask import Flask
from app.endpoints.user import user_route
from app.endpoints.registration import registration_route
from app.endpoints.login import login_route
from app.endpoints.article import article_route
from app.endpoints.admin import admin_route
from app.endpoints.course import course_route

# from app.endpoints.search import search_route


def add_routes(app: Flask):
    app.register_blueprint(user_route)
    app.register_blueprint(registration_route)
    app.register_blueprint(login_route)
    app.register_blueprint(article_route)
    app.register_blueprint(admin_route)
    app.register_blueprint(course_route)


# app.register_blueprint(search_route)
