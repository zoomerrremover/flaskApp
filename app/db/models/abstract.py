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
