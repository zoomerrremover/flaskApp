from app.db.models.concrete import Suggestion, SuggestionReaction
from app.db.service.common import DbService


class SuggestionDbService(DbService):
    MODEL = Suggestion
