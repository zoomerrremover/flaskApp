from flask import Flask
from app.routers import add_routes
from app.db.engine import engine, Base

app = Flask(__name__)
add_routes(app)
Base.metadata.create_all(engine)