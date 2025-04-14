from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from server,settings import DB_STRING

engine  = create_engine(DB_STRING, echo=True)

Session = sessionmaker(bind=engine)

session = Session()