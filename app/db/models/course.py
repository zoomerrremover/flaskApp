from .common import TextContentDbModel
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from dateetime import datetime
from sqlalchemy import UniqueConstraint, func


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
    def search_by_category(cls, limit: int, category: str):
        cls.get_filtered(limit, cls.category == category)
