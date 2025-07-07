from datetime import datetime

import pytest
from pydantic import ValidationError

from src.constants import ErrorsMsgEnum
from src.exceptions import InvalidDataError
from src.models import (SuggestionCreateModel, SuggestionGetModel,
                        SuggestionUpdateModel)

base_suggestion_create_data = {
    "title": "Improve Section 3",
    "text_content": "The explanation in section 3 \
        could be clearer with an additional example.",
    "article_id": 10,
}


base_suggestion_get_data = base_suggestion_create_data.copy()
base_suggestion_get_data.update(
    {
        "id": 1,
        "user_id": 101,
        "date_posted": datetime.now(),
        "stars_count": 1,
    }
)


base_suggestion_update_data = base_suggestion_create_data.copy()
base_suggestion_update_data.update({"id": 2})


base_suggestion_reaction_data = {"id": 3, "star": True}


def test_suggestion_create_model_valid_data():
    suggestion = SuggestionCreateModel(**base_suggestion_create_data)
    assert suggestion.title == "Improve Section 3"
    assert (
        suggestion.text_content
        == "The explanation in section 3\
         could be clearer with an additional example."
    )
    assert suggestion.article_id == 10


def test_suggestion_create_model_title_too_long():
    invalid_data = base_suggestion_create_data.copy()
    invalid_data["title"] = "A" * 999
    with pytest.raises(ValidationError) as exc_info:
        SuggestionCreateModel(**invalid_data)
    assert "title" in str(exc_info.value)


def test_suggestion_create_model_text_content_too_long():
    invalid_data = base_suggestion_create_data.copy()
    invalid_data["text_content"] = "A" * 8001  # Exceeds max_length of 8000
    with pytest.raises(ValidationError) as exc_info:
        SuggestionCreateModel(**invalid_data)
    assert "text_content" in str(exc_info.value)


def test_suggestion_create_model_invalid_title_content():
    invalid_data = base_suggestion_create_data.copy()
    invalid_data["title"] = "Title with <script> tags"
    with pytest.raises(InvalidDataError) as exc_info:
        SuggestionCreateModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_TEXT_CONTENT in str(exc_info.value)


def test_suggestion_create_model_invalid_text_content():
    invalid_data = base_suggestion_create_data.copy()
    invalid_data["text_content"] = "SQL: DELETE FROM articles;"
    with pytest.raises(InvalidDataError) as exc_info:
        SuggestionCreateModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_TEXT_CONTENT in str(exc_info.value)


def test_suggestion_create_model_missing_article_id():
    invalid_data = base_suggestion_create_data.copy()
    del invalid_data["article_id"]
    with pytest.raises(ValidationError) as exc_info:
        SuggestionCreateModel(**invalid_data)
    assert "article_id" in str(exc_info.value)


# --- Unit Tests for SuggestionGetModel ---


def test_suggestion_get_model_valid_data():
    suggestion_get = SuggestionGetModel(**base_suggestion_get_data)
    assert suggestion_get.id == base_suggestion_get_data["id"]
    assert suggestion_get.title == base_suggestion_get_data["title"]
    assert suggestion_get.text_content == base_suggestion_get_data["text_content"]
    assert suggestion_get.article_id == base_suggestion_get_data["article_id"]
    assert suggestion_get.user_id == base_suggestion_get_data["user_id"]
    assert isinstance(suggestion_get.date_posted, datetime)
    # Test with date_posted as None
    data_no_date = base_suggestion_get_data.copy()
    data_no_date["date_posted"] = None
    suggestion_get_no_date = SuggestionGetModel(**data_no_date)
    assert suggestion_get_no_date.date_posted is None


def test_suggestion_get_model_invalid_id():
    invalid_data = base_suggestion_get_data.copy()
    invalid_data["id"] = "not_an_int"
    with pytest.raises(ValidationError) as exc_info:
        SuggestionGetModel(**invalid_data)
    assert "id" in str(exc_info.value)


def test_suggestion_get_model_missing_user_id():
    invalid_data = base_suggestion_get_data.copy()
    del invalid_data["user_id"]
    with pytest.raises(ValidationError) as exc_info:
        SuggestionGetModel(**invalid_data)
    assert "user_id" in str(exc_info.value)


def test_suggestion_update_model_valid_data():
    suggestion_update = SuggestionUpdateModel(**base_suggestion_update_data)
    assert suggestion_update.id == base_suggestion_update_data["id"]
    assert suggestion_update.title == base_suggestion_update_data["title"]
    assert suggestion_update.text_content == base_suggestion_update_data["text_content"]
    assert suggestion_update.article_id == base_suggestion_update_data["article_id"]


def test_suggestion_update_model_invalid_id():
    invalid_data = base_suggestion_update_data.copy()
    invalid_data["id"] = "invalid_id"
    with pytest.raises(ValidationError) as exc_info:
        SuggestionUpdateModel(**invalid_data)
    assert "id" in str(exc_info.value)
