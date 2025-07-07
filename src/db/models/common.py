from abc import abstractmethod
from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import declarative_base

from src.db.engine import session

Base = declarative_base()


class LocalDbModelABC(Base):
    __abstract__ = True

    def as_dict(self):
        print({x: getattr(self, x) for x in self.__table__.c.keys()})
        return {x: getattr(self, x) for x in self.__table__.c.keys()}

    @classmethod
    def _delete(cls, *args) -> None:
        """
        Save a model instance.

        :return: Model instance
        """
        result = session.query(cls).filter(*args).delete()
        session.commit()
        return result

    def __str__(self):
        """
        Create a human readable version of a class instance.

        :return: self
        """
        obj_id = hex(id(self))
        columns = self.__table__.c.keys()

        values = ", ".join("%s=%r" % (n, getattr(self, n)) for n in columns)
        return "<%s %s(%s)>" % (obj_id, self.__class__.__name__, values)

    @classmethod
    def _get_list_all(cls):
        return session.query(cls).all()

    @classmethod
    def _get_filtered(cls, limit: int = 20, *args: object) -> object:
        """
        :param args:  cls.Column == Value
        :param limit:
        :return:
        """
        return session.query(cls).filter(*args).limit(limit).all()

    @classmethod
    def _get_filtered_all(cls, *args: object) -> object:
        """
        :param args:  cls.Column == Value
        :return:
        """
        return session.query(cls).filter(*args).all()

    @classmethod
    def _get_filtered_first(cls, *args: object) -> object:
        """
        :param args:  cls.Column == Value
        :return:
        """
        return session.query(cls).filter(*args).first()

    @classmethod
    def _update(cls, *args, **kwargs) -> int:
        request = session.query(cls).where(*args).update(kwargs)
        session.commit()
        return request

    @classmethod
    def create(cls, **kwargs):
        create_obj = cls(**kwargs)
        session.add(create_obj)
        session.commit()
        return create_obj


class IdDbModelABC(LocalDbModelABC):
    __abstract__ = True
    id: int = Column(Integer, primary_key=True)

    @classmethod
    def get_by_id(cls, id: int) -> object:
        return cls._get_filtered_first(cls.id == id)

    @classmethod
    def update_by_id(cls, model_id: int, **kwargs) -> int:
        return cls._update(cls.id == model_id, **kwargs)

    @classmethod
    def delete_by_id(cls, id: int):
        return cls._delete(cls.id == id)


class SearchableDbModelABC(IdDbModelABC):
    __abstract__ = True
    search_vector = Column(TSVECTOR)

    @classmethod
    def _search_vector_predicate(cls, text: str) -> object:
        return cls.search_vector.op("@@")(func.websearch_to_tsquery("english", text))

    @abstractmethod
    def update_search_vector(**kwargs) -> dict:
        pass

    @classmethod
    def update_by_id(cls, model_id: int, **kwargs) -> int:
        kwargs = cls.update_search_vector(**kwargs)
        return super().update_by_id(model_id, **kwargs)

    @classmethod
    def create(cls, **kwargs):
        kwargs = cls.update_search_vector(**kwargs)
        return super().create(**kwargs)


class TextContentDbModelABC(SearchableDbModelABC):
    __abstract__ = True
    title: str = Column(String, nullable=False)
    text_content: str = Column(String, nullable=False)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    def update_search_vector(**kwargs):
        title = kwargs["title"]
        text_content = kwargs["text_content"]
        kwargs["search_vector"] = func.to_tsvector(
            "english", title + " " + text_content
        )
        return kwargs

    @classmethod
    def get_by_user(cls, user_id: int, limit: int):
        return cls._get_filtered(limit, cls.user_id == user_id)
