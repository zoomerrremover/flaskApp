from flask import Flask
from .routers import add_routes

app = Flask(__name__)
add_routes(app)
