from src import Base, app, engine

Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run()
