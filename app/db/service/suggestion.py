from app.db.models.concrete import Suggestion, SuggestionReaction
from app.db.service.common import TextContentDbService


class SuggestionDbService(TextContentDbService):
    MODEL = Suggestion

    @classmethod
    def search_by_article(cls, article_id: int, limit: int):
        cls.MODEL.search_by_article(limit, article_id)
