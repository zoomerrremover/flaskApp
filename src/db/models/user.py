from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from .common import SearchableDbModel


class User(SearchableDbModel):
    __tablename__: str = "users"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String, nullable=False, unique=True)
    role: str = Column(String, nullable=False)
    date_registered: datetime = Column(TIMESTAMP)
    email: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    articles = relationship("Article", back_populates="author")
    courses = relationship("Course", back_populates="author")
    suggestions = relationship("Suggestion", back_populates="author")

    def update_search_vector(self):
        func.to_tsvector("english", self.username + " " + self.email)

    @classmethod
    def get_user_by_name(cls, username: str) -> object:
        return cls.get_filtered_first(cls.username == username)

    @classmethod
    def get_user_by_email(cls, email: str) -> object:
        return cls.get_filtered_first(cls.email == email)
