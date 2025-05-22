from app.db.models.concrete import Article
from app.db.service.common import DbService


class ArticleDbService(DbService):
    MODEL = Article
