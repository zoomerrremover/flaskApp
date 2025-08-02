from flask import Flask

from src.endpoints import (admin_route, article_route, common_route,
                           course_route, login_route, registration_route,
                           search_route, suggestion_route, user_route)


def add_routes(app: Flask):
    app.register_blueprint(admin_route)
    app.register_blueprint(article_route)
    app.register_blueprint(course_route)
    app.register_blueprint(login_route)
    app.register_blueprint(registration_route)
    app.register_blueprint(search_route)
    app.register_blueprint(suggestion_route)
    app.register_blueprint(user_route)
    app.register_blueprint(common_route)
