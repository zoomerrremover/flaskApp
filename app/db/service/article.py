from app.db.models.models import Article
from datetime import datetime

def create_article(title: str, text_content: str, user_id: int,course_id: int, date_posted: datetime, next_article: int,
                   previous_article: int):
    return (
        Article(
            title=title,
            text_content=text_content,
            date_posted=date_posted,
            user_id=user_id,
            course_id=course_id,
            next_article=next_article,
            previous_article=previous_article
        ).save()
    )


def get_article_by_id(article_id: int):
    return Article.get_by_id(article_id)


def update_article_by_id(article_id: int, **kwargs):
    return Article.update_by_id(article_id, **kwargs)


def delete_article_by_id(article_id):
    return Article.delete_by_id(article_id)
