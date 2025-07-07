from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, Integer, String, func
from sqlalchemy.orm import relationship

from src.db.models.common import SearchableDbModelABC


class User(SearchableDbModelABC):
    __tablename__: str = "users"
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String, nullable=False, unique=True)
    role: str = Column(String, nullable=False)
    date_registered: datetime = Column(TIMESTAMP, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    articles = relationship("Article", back_populates="author")
    courses = relationship("Course", back_populates="author")
    suggestions = relationship("Suggestion", back_populates="author")
    reactions = relationship("SuggestionReaction", back_populates="user")

    def update_search_vector(**kwargs):
        username = kwargs["username"]
        email = kwargs["email"]
        kwargs["search_vector"] = func.to_tsvector("english", username + " " + email)
        return kwargs

    @classmethod
    def get_user_by_name(cls, username: str) -> object:
        return cls._get_filtered_first(cls.username == username)

    @classmethod
    def get_user_by_email(cls, email: str) -> object:
        return cls._get_filtered_first(cls.email == email)

    @classmethod
    def search(cls, search_query: str, limit: int):
        return cls._get_filtered(limit, cls._search_vector_predicate(search_query))
