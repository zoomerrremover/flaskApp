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


class IdDbModel(LocalDbModel):
    __abstract__ = True
    id: int = Column(Integer, primary_key=True)

    @classmethod
    def get_all_models(cls):
        return cls.get_list_all()

    @classmethod
    def get_by_id(cls, id: int) -> object:
        return cls.get_filtered_first(cls.id == id)

    @classmethod
    def update_by_id(cls, model_id: int, **kwargs) -> int:
        return cls.update(cls.id == model_id, **kwargs)

    @classmethod
    def delete_by_id(cls, id: int):
        cls.delete(cls.id == id)


class TextContentDbModel(IdDbModel):
    __abstract__ = True
    title: str = Column(String, nullable=False)
    text_content: str = Column(String, nullable=False)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)

    @classmethod
    def search_by_content(cls, content: str):
        return str_compare(cls.title, content,70) or str_compare(cls.text_content, content, 20)

    @classmethod
    def search_by_user(cls, user_id: int):
        return cls.get_filtered_all(cls.user_id == user_id)

    @classmethod
    def search_within_date_range(cls, start_date: datetime ,end_date: datetime):
        filter_condition = (cls.created_at >= start_date) & (cls.created_at <= end_date)
        return cls.get_filtered_all(filter_condition)


class User(IdDbModel):
    __tablename__: str = 'users'
    id: int = Column(Integer, primary_key=True)
    username: str = Column(String,nullable=False)
    role: str = Column(String,nullable=False)
    email: str = Column(String,nullable=False)
    password: str = Column(String,nullable=False)
    articles = relationship('Article', back_populates="author")
    courses = relationship('Course', back_populates="author")

    @classmethod
    def search_users_by_username(cls, username: str) -> object:
        return cls.get_filtered_all(str_compare(cls.username, username, 20))

    @classmethod
    def search_users_by_email(cls, email: str) -> object:
        return cls.get_filtered_all(str_compare(cls.email, email, 80))

    @classmethod
    def search_users_by_role(cls, role: str) -> object:
        return cls.get_filtered_all(cls.role == role)

    @classmethod
    def get_user_by_name(cls, username: str) -> object:
        return cls.get_filtered_first(cls.username == username)

    @classmethod
    def get_user_by_email(cls, email: str) -> object:
        return cls.get_filtered_first(cls.email == email)


class Course(TextContentDbModel):
    __tablename__ = "courses"
    id: int = Column(Integer, primary_key=True)
    title: str = Column(String, nullable=False)
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
    title: str = Column(String, nullable=False)
    text_content: str = Column(String, nullable=False)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey('users.id'), nullable=False)
    author = relationship('User', back_populates="articles")
    course_id: int  = Column(Integer, ForeignKey('courses.id'), nullable=False)
    course = relationship('Course', back_populates="articles")
    next_article: int = Column(Integer, ForeignKey('articles.id'))
    previous_article: int = Column(Integer, ForeignKey('articles.id'))

    @classmethod
    def search_by_course(cls, course_id: int):
        cls.get_filtered_all(cls.course_id == course_id)
