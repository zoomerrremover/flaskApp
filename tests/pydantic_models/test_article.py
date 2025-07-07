from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from src.constants import ErrorsMsgEnum
from src.exceptions import InvalidDataError
from src.models import ArticleCreateModel, ArticleGetModel, ArticleUpdateModel

base_article_create_data = {
    "title": "My Awesome Article",
    "text_content": "This is some content for my article.",
    "course_id": 101,
}


base_article_get_data = base_article_create_data.copy()
base_article_get_data.update(
    {"id": 1, "user_id": 5, "date_posted": datetime.now(timezone.utc)}
)


base_article_update_data = base_article_create_data.copy()
base_article_update_data.update({"id": 10})


def test_article_create_model_valid_data():
    # Test with all fields
    article_data_full = base_article_create_data.copy()
    article_data_full.update({"next_article": 2, "previous_article": 0})
    article = ArticleCreateModel(**article_data_full)
    assert article.title == "My Awesome Article"
    assert article.text_content == "This is some content for my article."
    assert article.course_id == 101
    assert article.next_article == 2
    assert article.previous_article == 0
    # Test with optional fields as None (using the base fixture directly)
    article_no_optional = ArticleCreateModel(**base_article_create_data)
    assert article_no_optional.next_article is None
    assert article_no_optional.previous_article is None


def test_article_create_model_title_too_long():
    invalid_data = base_article_create_data.copy()
    invalid_data["title"] = "A" * 999
    with pytest.raises(ValidationError) as exc_info:
        ArticleCreateModel(**invalid_data)
    assert "title" in str(exc_info.value)


def test_article_create_model_text_content_too_long():
    invalid_data = base_article_create_data.copy()
    invalid_data["text_content"] = "A" * 8001  # Exceeds max_length of 8000
    with pytest.raises(ValidationError) as exc_info:
        ArticleCreateModel(**invalid_data)
    assert "text_content" in str(exc_info.value)


def test_article_create_model_invalid_title_content():
    invalid_data = base_article_create_data.copy()
    invalid_data["title"] = "<script>alert('xss')</script>"
    with pytest.raises(InvalidDataError) as exc_info:
        ArticleCreateModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_TEXT_CONTENT in str(exc_info.value)


def test_article_create_model_invalid_text_content():
    invalid_data = base_article_create_data.copy()
    invalid_data["text_content"] = "This content has <unsafe> tags."
    with pytest.raises(InvalidDataError) as exc_info:
        ArticleCreateModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_TEXT_CONTENT in str(exc_info.value)


def test_article_get_model_valid_data():
    article_get = ArticleGetModel(**base_article_get_data)
    assert article_get.id == base_article_get_data["id"]
    assert article_get.title == base_article_get_data["title"]
    assert article_get.text_content == base_article_get_data["text_content"]
    assert article_get.course_id == base_article_get_data["course_id"]
    assert article_get.user_id == base_article_get_data["user_id"]
    assert article_get.date_posted == base_article_get_data["date_posted"]
    # Test with date_posted as None
    data_no_date = base_article_get_data.copy()
    data_no_date["date_posted"] = None
    article_get_no_date = ArticleGetModel(**data_no_date)
    assert article_get_no_date.date_posted is None


def test_article_get_model_invalid_id():
    invalid_data = base_article_get_data.copy()
    invalid_data["id"] = "not_an_int"  # Invalid ID type
    with pytest.raises(ValidationError) as exc_info:
        ArticleGetModel(**invalid_data)
    assert "id" in str(exc_info.value)


def test_article_update_model_valid_data():
    article_update = ArticleUpdateModel(**base_article_update_data)
    assert article_update.id == base_article_update_data["id"]
    assert article_update.title == base_article_update_data["title"]
    assert article_update.text_content == base_article_update_data["text_content"]
    assert article_update.course_id == base_article_update_data["course_id"]
    assert article_update.next_article is None
    assert article_update.previous_article is None


def test_article_update_model_invalid_id():
    invalid_data = base_article_update_data.copy()
    invalid_data["id"] = "invalid_id_string"  # Invalid ID type
    with pytest.raises(ValidationError) as exc_info:
        ArticleUpdateModel(**invalid_data)
    assert "id" in str(exc_info.value)
