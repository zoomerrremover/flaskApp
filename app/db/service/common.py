from app.db.models.abstract import IdDbModel


class DbService:
    __abstract__ = True
    MODEL: IdDbModel

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
