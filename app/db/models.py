from datetime import datetime

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from app.db.engine import engine
from app.db.engine import session

Base = declarative_base()

class LocalDbModel(Base):
    __abstract__ = True

    def as_dict(self):
        return {x: getattr(self, x) for x in self.__table__.c.keys()}

    def save(self):
        """
        Save a model instance.

        :return: Model instance
        """
        session.add(self)
        session.commit()

        return self

    @classmethod
    def delete(cls, *args) -> None:
        """
        Save a model instance.

        :return: Model instance
        """
        session.query(cls).filter(*args).delete()
        session.commit()

    def __str__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ', '.join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return '<%s %s(%s)>' % (obj_id, self.__class__.__name__, values)

    @classmethod
    def get_list_all(cls):
        return session.query(cls).all()

    @classmethod
    def get_filtered_all(cls, *args: object) -> object:
        """
        :param args:  cls.Column == Value
        :return:
        """
        return session.query(cls).filter(*args).all()

    @classmethod
    def get_filtered_first(cls, *args: object) -> object:
        """
        :param args:  cls.Column == Value
        :return:
        """
        return session.query(cls).filter(*args).first()

    @classmethod
    def update(cls, *args, **kwargs) -> int:
        request = session.query(cls).where(*args).update(kwargs)
        session.commit()
        return request

class User(LocalDbModel):
    __tablename__ = 'users'

    id:int = Column(Integer, primary_key=True)
    username:str = Column(String,nullable=False)
    role:str = Column(String,nullable=False)
    email:str = Column(String,nullable=False)
    password:str = Column(String,nullable=False)
    articles = relationship("Article",back_populates = 'author')
    suggestions = relationship("Suggestion", back_populates='author')

    @classmethod
    def get_user_by_id(cls, user_id:int):
        return cls.get_filtered_first(cls.id == user_id)

    @classmethod
    def get_filtered_users(cls, *args: object):
        return cls.get_filtered_all(*args)

    @classmethod
    def get_filtered_user(cls, *args: object):
        return cls.get_filtered_first(*args)

    @classmethod
    def get_users(cls):
        return cls.get_list_all()

    @classmethod
    def delete_user_by_id(cls,user_id:int):
        cls.delete(cls.id == user_id)

    @classmethod
    def update_user_by_id(cls, user_id:int, **kwargs) -> int:
        return cls.update(cls.id == user_id, **kwargs)

class Course(LocalDbModel):
    __tablename__ = "courses"
    id:int = Column(Integer,primary_key = True)
    title:str = Column(String,nullable = False)
    category: str = Column(String, nullable=False)
    text_content:str = Column(String,nullable = False)
    date_posted:datetime = Column(TIMESTAMP,nullable = False)
    articles = relationship("Article", back_populates='course')

    @classmethod
    def get_course_by_id(cls,course_id:int):
        return cls.get_filtered_first(cls,course_id)

    @classmethod
    def delete_course_by_id(cls,course_id:int):
        return cls.delete_course_by_id(course_id)

    @classmethod
    def update_course_by_id(cls,course_id:int,**kwargs):
        cls.update_course_by_id(course_id,**kwargs)

    @classmethod
    def get_courses(cls):
        cls.get_list_all()

class Article(LocalDbModel):
    __tablename__ = "articles"
    id:int = Column(Integer,primary_key = True)
    title:str = Column(String,nullable = False)
    text_content:str = Column(String,nullable = False)
    date_posted:datetime = Column(TIMESTAMP,nullable = False)
    course_id: int = Column(Integer, ForeignKey('courses.id'))
    user_id: int = Column(Integer, ForeignKey('users.id'))
    author = relationship('User',back_populates="articles")
    course = relationship("Course", back_populates='articles')
    suggestions = relationship("Suggestion", back_populates='article')

    @classmethod
    def get_article_by_id(cls,article_id:int):
        return cls.get_filtered_first(cls,article_id)

    @classmethod
    def delete_article_by_id(cls,article_id:int):
        return cls.delete_article_by_id(article_id)

    @classmethod
    def update_article_by_id(cls,article_id:int,**kwargs):
        cls.update_article_by_id(article_id,**kwargs)

    @classmethod
    def get_articles(cls):
        cls.get_list_all()

class Suggestion(LocalDbModel):
    __tablename__ = "suggestions"
    id:int = Column(Integer,primary_key = True)
    title:str = Column(String,nullable = False)
    text_content:str = Column(String,nullable = False)
    date_posted:datetime = Column(TIMESTAMP,nullable = False)
    up_vote = Column(Integer,nullable = False)
    down_vote = Column(Integer,nullable = False)
    article_id: int = Column(Integer, ForeignKey('articles.id'))
    user_id: int = Column(Integer, ForeignKey('users.id'))
    author = relationship('User',back_populates="suggestions")
    article = relationship("Article", back_populates='suggestions')

    @classmethod
    def get_suggestion_by_id(cls,suggestion_id:int):
        return cls.get_filtered_first(cls,suggestion_id)

    @classmethod
    def delete_suggestion_by_id(cls,suggestion_id:int):
        return cls.delete_suggestion_by_id(suggestion_id)

    @classmethod
    def update_suggestion_by_id(cls,suggestion_id:int,**kwargs):
        cls.update_suggestion_by_id(suggestion_id,**kwargs)

    @classmethod
    def get_suggestions(cls):
        cls.get_list_all()



Base.metadata.create_all(engine)





