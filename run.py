from app.app import app
from app.db import engine, Base

Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run(debug=True)
