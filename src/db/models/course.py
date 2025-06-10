from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import UniqueConstraint, func
from src.db.models.common import TextContentDbModel


class Course(TextContentDbModel):
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

    def update_search_vector(self):
        func.to_tsvector(
            "english", self.title + " " + self.text_content + " " + self.category
        )

    @classmethod
    def get_by_category(cls, category: str):
        cls._get_filtered_all(cls.category == category)

    @classmethod
    def search(cls, search_query: str, limit: int):
        return cls._get_filtered(limit, cls._search_vector_predicate(search_query))
