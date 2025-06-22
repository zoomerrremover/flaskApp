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
from sqlalchemy.ext.hybrid import hybrid_property
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
    reactions = relationship("SuggestionReaction", back_populates="suggestion")

    def as_dict(self):
        ret_val = super().as_dict()
        ret_val.update({"stars_count": self.stars_count})
        return ret_val

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

    @hybrid_property
    def stars_count(self):
        """
        Python-side access: Returns the number of likes for this post.
        This iterates over the 'likes' collection (list of Like objects).
        """
        return len(self.reactions)

    @stars_count.expression
    def stars_count(cls):
        """
        SQL-side access: Returns the number of likes for this post using a SQL COUNT.
        This now queries the 'Like' class directly, which maps to the 'likes' table.
        """
        from sqlalchemy import select  # Import select for modern SQLAlchemy queries

        return (
            select(
                func.count(SuggestionReaction.user_id)
            )  # COUNT user_id from the Like table
            .where(
                SuggestionReaction.suggestion_id == cls.id
            )  # Filter by this Post's ID
            .scalar_subquery()  # Makes it a scalar subquery for use in SELECT list
        )


class SuggestionReaction(LocalDbModel):
    __tablename__ = "suggestion_reactions"
    suggestion_id: int = Column(
        Integer, ForeignKey("suggestions.id"), nullable=False, primary_key=True
    )
    user_id: int = Column(
        Integer, ForeignKey("users.id"), nullable=False, primary_key=True
    )

    user = relationship("User", back_populates="reactions")
    suggestion = relationship("Suggestion", back_populates="reactions")

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

