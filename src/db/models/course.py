from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.db.models.common import TextContentDbModelABC


class Course(TextContentDbModelABC):
    __tablename__ = "courses"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False, unique=True)
    text_content: str = Column(String, nullable=False)
    date_created: datetime = Column(TIMESTAMP)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="courses")
    category: str = Column(String, nullable=False)
    articles = relationship("Article", back_populates="course")

    @classmethod
    def get_course_by_category(cls, category: str, limit: int):
        return cls._get_filtered(limit, cls.category == category)

    @classmethod
    def search(cls, search_query: str, limit: int):
        return cls._get_filtered(limit, cls._search_vector_predicate(search_query))
