from src import app, Base, engine

Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run(debug=True)
