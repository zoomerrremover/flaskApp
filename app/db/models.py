from datetime import datetime

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey

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
    password:str = Column(String,nullable=False)
    posts = relationship("Post",back_populates = 'author')

    @classmethod
    def get_user_by_id(cls, user_id:int):
        return cls.get_filtered_first(cls.id == user_id)

    @classmethod
    def get_users(cls):
        return cls.get_list_all()

    @classmethod
    def delete_user_by_id(cls,user_id:int):
        cls.delete(cls.id == user_id)

    @classmethod
    def update_user_by_id(cls, user_id:int, **kwargs) -> int:
        return cls.update(cls.id == user_id, **kwargs)

class Post(LocalDbModel):
    id:int = Column(Integer,primary_key = True)
    title:str = Column(String,nullable = False)
    text_content:str = Column(String,nullable = False)
    date_posted:datetime = Column(TIMESTAMP,nullable = False)
    author = relationship('User',back_populates="author")

    @classmethod
    def get_post_by_id(cls,post_id:int):
        return cls.get_filtered_first(cls,post_id)

    @classmethod
    def search_posts_by_content(cls,func):
        return cls.get_filtered_all(func(cls.text_content))

    @classmethod
    def delete_post_by_id(cls,post_id:int):
        return cls.delete_post_by_id(post_id)

    @classmethod
    def update_post_by_id(cls,post_id:int,**kwargs):
        cls.update_post_by_id(post_id,**kwargs)

    @classmethod
    def get_posts(cls):
        cls.get_list_all()






