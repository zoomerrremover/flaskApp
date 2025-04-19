from app import app
from api.posts import post_route
from api.user import user_route
from api.registration import registration_route

app.register_blueprint(post_route, url_prefix='/post')
app.register_blueprint(user_route, url_prefix='/user')
app.register_blueprint(registration_route, url_prefix='/register')