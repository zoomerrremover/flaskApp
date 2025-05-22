from app.db.models.abstract import TextContentDbModel, SearchableDbModel, TextContentDbModel


class DbService:
    __abstract__ = True
    MODEL: SearchableDbModel

    @classmethod
    def create(cls, **kwargs):
        return cls.MODEL(**kwargs).save()

    @classmethod
    def get_by_id(cls, model_id: int):
        return cls.MODEL.get_by_id(model_id)

    @classmethod
    def update(cls, model_id: int, **kwargs):
        return cls.MODEL.update_by_id(model_id, **kwargs)

    @classmethod
    def delete(cls, model_id: int):
        return cls.MODEL.delete_by_id(model_id)

    @classmethod
    def search_by_query(cls, query: str, limit: int = 20):
        return cls.MODEL.search_by_vector(query, limit)


class TextContentDbService(DbService):
    __abstract__ = True
    MODEL: TextContentDbModel

    @classmethod
    def search_by_user(cls, user_id: int, limit: int):
        return cls.MODEL.search_by_user(limit, user_id)
