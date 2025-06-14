from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import TSVECTOR
from datetime import datetime
from sqlalchemy import func, event
from src.db.engine import session

Base = declarative_base()


class LocalDbModel(Base):
    __abstract__ = True

    def as_dict(self):
        print({x: getattr(self, x) for x in self.__table__.c.keys()})
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
    def _delete(cls, *args) -> None:
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


class IdDbModel(LocalDbModel):
    __abstract__ = True
    id: int = Column(Integer, primary_key=True)

    @classmethod
    def get_all_models(cls):
        return cls._get_list_all()

    @classmethod
    def get_by_id(cls, id: int) -> object:
        return cls._get_filtered_first(cls.id == id)

    @classmethod
    def update_by_id(cls, model_id: int, **kwargs) -> int:
        return cls._update(cls.id == model_id, **kwargs)

    @classmethod
    def delete_by_id(cls, id: int):
        cls._delete(cls.id == id)


class SearchableDbModel(IdDbModel):
    __abstract__ = True
    search_vector = Column(TSVECTOR)

    @classmethod
    def _search_vector_predicate(cls, text: str) -> object:
        return cls.search_vector.op("@@")(func.websearch_to_tsquery("english", text))

    def update_search_vector(self):
        pass

    @classmethod
    def update_by_id(cls, model_id: int, **kwargs) -> int:
        model = cls.get_by_id(model_id)
        model.update_search_vector()
        return super().update_by_id(model_id, **kwargs)


@event.listens_for(SearchableDbModel, "before_insert", propagate=True)
def trigger_search_vector_update(mapper, connection, target):
    target.update_search_vector()


class TextContentDbModel(SearchableDbModel):
    __abstract__ = True
    title: str = Column(String, nullable=False)
    text_content: str = Column(String, nullable=False)
    date_posted: datetime = Column(TIMESTAMP)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)

    def update_search_vector(self):
        self.search_vector = func.to_tsvector(
            "english", self.title + " " + self.text_content
        )

    @classmethod
    def get_by_user(cls, user_id: int, limit: int):
        return cls._get_filtered(limit, cls.user_id == user_id)
