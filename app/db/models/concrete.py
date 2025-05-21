from enum import unique
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.dialects.postgresql import TSVECTOR
from datetime import datetime
from app.db.models.abstract import IdDbModel, TextContentDbModel


class User(IdDbModel):
    __tablename__: str = 'users'
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String, nullable=False, unique=True)
    role: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    password: str = Column(String, nullable=False)
    articles = relationship('Article', back_populates="author")
    courses = relationship('Course', back_populates="author")
    suggestions = relationship('Suggestion', back_populates="author")

    @classmethod
    def get_user_by_name(cls, username: str) -> object:
        return cls.get_filtered_first(cls.username == username)

    @classmethod
    def get_user_by_email(cls, email: str) -> object:
        return cls.get_filtered_first(cls.email == email)


class Course(TextContentDbModel):
    __tablename__ = "courses"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False, unique=True)
    text_content: str = Column(String, nullable=False)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User', back_populates="courses")
    category: str = Column(String, nullable=False)
    articles = relationship('Article', back_populates="course")

    @classmethod
    def search_by_category(cls, category: str):
        cls.get_filtered_all(cls.category == category)


class Article(TextContentDbModel):
    __tablename__ = "articles"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False, unique=True)
    text_content: str = Column(String, nullable=False)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User', back_populates="articles")
    course_id: int = Column(Integer, ForeignKey('courses.id'), nullable=False)
    course = relationship('Course', back_populates="articles")
    next_article: int = Column(Integer, ForeignKey('articles.id'))
    previous_article: int = Column(Integer, ForeignKey('articles.id'))
    suggestions = relationship('Suggestion', back_populates="article")
    search_vector = Column(TSVECTOR)

    @classmethod
    def search_by_course(cls, course_id: int):
        cls.get_filtered_all(cls.course_id == course_id)


class Suggestion(TextContentDbModel):
    __tablename__ = "suggestions"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False)
    text_content: str = Column(String, nullable=False)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User', back_populates="suggestions")
    article_id: int = Column(Integer, ForeignKey('articles.id'), nullable=False)
    article = relationship('Article', back_populates="suggestions")

    @classmethod
    def search_by_article(cls, article_id: int):
        cls.get_filtered_all(cls.article_id == article_id)


class SuggestionReaction(IdDbModel):
    __tablename__ = "suggestion_reactions"
    id: int = Column(Integer, primary_key=True)
    like: bool = Column(Boolean, nullable=False)
    suggestion_id: int = Column(Integer, ForeignKey('suggestions.id'), nullable=False)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)

    @classmethod
    def get_reaction(cls, suggestion_id: int, user_id: int):
        return cls.get_filtered_first(cls.suggestion_id == suggestion_id and cls.user_id == user_id)

    @classmethod
    def get_reactions_by_user(cls, user_id: int):
        return cls.get_filtered_all(cls.user_id == user_id)

    @classmethod
    def get_reactions_by_suggestion(cls, suggestion_id: int):
        return cls.get_filtered_all(cls.suggestion_id == suggestion_id)

    @classmethod
    def update_reaction(cls, suggestion_id: int, user_id: int, like: bool):
        return cls.update(cls.suggestion_id == suggestion_id and cls.user_id == user_id, {"like": like})

    @classmethod
    def delete_reaction(cls, suggestion_id: int, user_id: int):
        return cls.delete(cls.suggestion_id == suggestion_id and cls.user_id == user_id)


#class CommentSuggestion(IdDbModel):
 #   id: int = Column(Integer, primary_key=True)
#    suggestion_id: int = Column(Integer, ForeignKey('suggestions.id'), nullable=False)
#    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
#    comment_id: int = Column(Integer, ForeignKey('comment.id'), nullable=False)
