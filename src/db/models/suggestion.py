from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    ForeignKey,
    Boolean,
    UniqueConstraint,
    func,
)
from datetime import datetime
from src.db.models.common import TextContentDbModel, LocalDbModel


class Suggestion(TextContentDbModel):
    __tablename__ = "suggestions"
    __table_args__ = (
        UniqueConstraint(
            "article_id", "title", name="unique_suggestion_title_within_article"
        ),
    )
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False)
    text_content: str = Column(String, nullable=False)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", back_populates="suggestions")
    article_id: int = Column(Integer, ForeignKey("articles.id"), nullable=False)
    article = relationship("Article", back_populates="suggestions")

    @classmethod
    def get_by_article(cls, article_id: int, limit: int):
        return cls._get_filtered(limit, cls.article_id == article_id)

    @classmethod
    def search(cls, search_query: str, article_id: int, limit: int):
        return cls._get_filtered(
            limit,
            cls.article_id == article_id,
            cls._search_vector_predicate(search_query),
        )


class SuggestionReaction(LocalDbModel):
    __tablename__ = "suggestion_reactions"
    suggestion_id: int = Column(
        Integer, ForeignKey("suggestions.id"), nullable=False, primary_key=True
    )
    user_id: int = Column(
        Integer, ForeignKey("users.id"), nullable=False, primary_key=True
    )

    @classmethod
    def get_reaction(cls, suggestion_id: int, user_id: int):
        return cls._get_filtered_first(
            cls.suggestion_id == suggestion_id, cls.user_id == user_id
        )

    @classmethod
    def get_reactions_by_user(cls, user_id: int):
        return cls._get_filtered_all(cls.user_id == user_id)

    @classmethod
    def get_reactions_by_suggestion(cls, suggestion_id: int):
        return cls._get_filtered_all(cls.suggestion_id == suggestion_id)

    @classmethod
    def delete_reaction(cls, suggestion_id: int, user_id: int):
        return cls._delete(cls.suggestion_id == suggestion_id, cls.user_id == user_id)
