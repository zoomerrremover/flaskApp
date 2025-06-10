from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import UniqueConstraint, func
from src.db.models.common import TextContentDbModel


class Article(TextContentDbModel):
    __tablename__ = "articles"
    __table_args__ = (
        UniqueConstraint(
            "course_id", "title", name="unique_article_title_within_course"
        ),
    )
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False)
    text_content: str = Column(String, nullable=False)
    date_created: datetime = Column(TIMESTAMP)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="articles")
    course_id: int = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="articles")
    next_article: int = Column(Integer, ForeignKey("articles.id"))
    previous_article: int = Column(Integer, ForeignKey("articles.id"))
    suggestions = relationship("Suggestion", back_populates="article")

    def update_search_vector(self):
        func.to_tsvector("english", self.title + " " + self.text_content)

    @classmethod
    def get_by_course(cls, limit: int, course_id: int):
        cls._get_filtered_all(cls.course_id == course_id)

    @classmethod
    def search(cls, course_id: int, search_string: str, limit: int):
        cls._get_filtered(
            limit,
            cls.course_id == course_id and cls._search_vector_predicate(search_string),
        )
