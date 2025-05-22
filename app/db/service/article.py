from app.db.models.concrete import Article
from app.db.service.common import TextContentDbService


class ArticleDbService(TextContentDbService):
    MODEL = Article

    @classmethod
    def search_by_course(cls, article_id: int, limit: int):
        return cls.MODEL.search_by_course(limit, article_id)
