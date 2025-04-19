from flask import Flask
from app.routers import add_routes

app = Flask(__name__)
add_routes(app)