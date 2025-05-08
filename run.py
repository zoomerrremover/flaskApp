from app.app import app
from app.db.engine import engine
from app.db.models import Base

Base.metadata.create_all(engine)

if __name__ == '__main__':
    app.run(debug=True)
