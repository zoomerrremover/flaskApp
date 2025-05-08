from app.db.models import Article
from app.models.article import ArticleGet
from datetime import datetime

def create_article(user_id: int, title: str, text_content: str, date_posted: datetime):
    return Article(title=title, text_content=text_content, date_posted=date_posted, user_id=user_id).save()


def get_article_by_id(article_id: int):
    article = Article.get_article_by_id(article_id)
    return ArticleGet(title=article.title, author=article.user_id, text_content=article.text_content,
                      date_posted=article.date_posted)


def update_article_by_id(article_id: int, **kwargs):
    return Article.update_article_by_id(article_id, **kwargs)


def delete_article_by_id(article_id):
    return Article.delete_article_by_id(article_id)