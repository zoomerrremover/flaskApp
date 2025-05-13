from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from app.db.engine import session
from app.common import str_compare
from datetime import datetime

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
    __tablename__: str = 'users'
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String,nullable=False)
    role: str = Column(String,nullable=False)
    email: str = Column(String,nullable=False)
    password: str = Column(String,nullable=False)
    articles = relationship('Article', back_populates="author")

    @classmethod
    def get_users(cls):
        return cls.get_list_all()

    @classmethod
    def get_users_by_username(cls, username: str) -> object:
        return cls.get_filtered_all(str_compare(cls.username, username, 20))

    @classmethod
    def get_users_by_email(cls, email: str) -> object:
        return cls.get_filtered_all(str_compare(cls.email, email, 80))

    @classmethod
    def get_users_by_role(cls, role: str) -> object:
        return cls.get_filtered_all(cls.role == role)

    @classmethod
    def get_user_by_id(cls, user_id: int) -> object:
        return cls.get_filtered_first(cls.id == user_id)

    @classmethod
    def get_user_by_exact_name(cls, username: str) -> object:
        return cls.get_filtered_first(cls.username == username)

    @classmethod
    def get_user_by_exact_email(cls, email: str) -> object:
        return cls.get_filtered_first(cls.email == email)

    @classmethod
    def update_user_by_id(cls, user_id: int, **kwargs) -> int:
        return cls.update(cls.id == user_id, **kwargs)

    @classmethod
    def delete_user_by_id(cls, user_id: int):
        cls.delete(cls.id == user_id)

class Article(LocalDbModel):
    __tablename__ = "articles"
    id: int = Column(Integer, primary_key = True)
    title: str = Column(String, nullable = False)
    text_content: str = Column(String, nullable = False)
    date_posted: datetime = Column(TIMESTAMP, nullable = False)
    user_id: int = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', back_populates="articles")

    @classmethod
    def get_article_by_id(cls,article_id: int):
        return cls.get_filtered_first(cls.id == article_id)

    @classmethod
    def get_articles(cls):
        return cls.get_list_all()

    @classmethod
    def search_articles_by_titles(cls, article_title: str):
        return cls.get_filtered_all(str_compare(article_title, cls.title,50))

    @classmethod
    def delete_article_by_id(cls,article_id: int):
        return cls.delete(article_id)

    @classmethod
    def update_article_by_id(cls,article_id: int, **kwargs):
        return cls.update(article_id, **kwargs)
