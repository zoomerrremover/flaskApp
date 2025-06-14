import pytest
from datetime import datetime
from pydantic import ValidationError
from src.models import SuggestionCreateModel, SuggestionGetModel, SuggestionUpdateModel
from src.exceptions import InvalidDataError
from src.constants import ErrorsMsgEnum


def test_suggestion_create_model_valid_data(base_suggestion_create_data):
    """
    Tests that SuggestionCreateModel can be successfully instantiated with valid data.
    """
    suggestion = SuggestionCreateModel(**base_suggestion_create_data)

    assert suggestion.title == "Improve Section 3"
    assert (
        suggestion.text_content
        == "The explanation in section 3 could be clearer with an additional example."
    )
    assert suggestion.article_id == 10


def test_suggestion_create_model_title_too_long(base_suggestion_create_data):
    """
    Tests that SuggestionCreateModel raises ValidationError when title exceeds max_length.
    """
    base_suggestion_create_data["title"] = "A" * 33  # Exceeds max_length of 32
    with pytest.raises(ValidationError) as exc_info:
        SuggestionCreateModel(**base_suggestion_create_data)
    assert "title" in str(exc_info.value)


def test_suggestion_create_model_text_content_too_long(base_suggestion_create_data):
    """
    Tests that SuggestionCreateModel raises ValidationError when text_content exceeds max_length.
    """
    base_suggestion_create_data["text_content"] = (
        "A" * 8001
    )  # Exceeds max_length of 8000
    with pytest.raises(ValidationError) as exc_info:
        SuggestionCreateModel(**base_suggestion_create_data)
    assert "text_content" in str(exc_info.value)


def test_suggestion_create_model_invalid_title_content(base_suggestion_create_data):
    """
    Tests that SuggestionCreateModel's custom validator rejects invalid characters in title.
    """
    base_suggestion_create_data["title"] = "Title with <script> tags"
    with pytest.raises(InvalidDataError) as exc_info:
        SuggestionCreateModel(**base_suggestion_create_data)
    assert ErrorsMsgEnum.ERROR_TEXT_CONTENT in str(exc_info.value)


def test_suggestion_create_model_invalid_text_content(base_suggestion_create_data):
    """
    Tests that SuggestionCreateModel's custom validator rejects invalid characters in text_content.
    """
    base_suggestion_create_data["text_content"] = "SQL: DELETE FROM articles;"
    with pytest.raises(InvalidDataError) as exc_info:
        SuggestionCreateModel(**base_suggestion_create_data)
    assert ErrorsMsgEnum.ERROR_TEXT_CONTENT in str(exc_info.value)


def test_suggestion_create_model_missing_article_id(base_suggestion_create_data):
    """
    Tests that SuggestionCreateModel raises ValidationError if article_id is missing.
    """
    del base_suggestion_create_data["article_id"]
    with pytest.raises(ValidationError) as exc_info:
        SuggestionCreateModel(**base_suggestion_create_data)

    assert "article_id" in str(exc_info.value)


# --- Unit Tests for SuggestionGetModel ---


def test_suggestion_get_model_valid_data(base_suggestion_get_data):
    """
    Tests that SuggestionGetModel can be successfully instantiated with valid data.
    """
    suggestion_get = SuggestionGetModel(**base_suggestion_get_data)

    assert suggestion_get.id == base_suggestion_get_data["id"]
    assert suggestion_get.title == base_suggestion_get_data["title"]
    assert suggestion_get.text_content == base_suggestion_get_data["text_content"]
    assert suggestion_get.article_id == base_suggestion_get_data["article_id"]
    assert suggestion_get.user_id == base_suggestion_get_data["user_id"]
    assert isinstance(suggestion_get.date_posted, datetime)
    assert suggestion_get.stars_count == 10

    # Test with date_posted as None
    base_suggestion_get_data["date_posted"] = None
    suggestion_get_no_date = SuggestionGetModel(**base_suggestion_get_data)
    assert suggestion_get_no_date.date_posted is None


def test_suggestion_get_model_invalid_id(base_suggestion_get_data):
    """
    Tests that SuggestionGetModel raises ValidationError for invalid ID type.
    """
    base_suggestion_get_data["id"] = "not_an_int"
    with pytest.raises(ValidationError) as exc_info:
        SuggestionGetModel(**base_suggestion_get_data)
    assert "id" in str(exc_info.value)


def test_suggestion_get_model_missing_user_id(base_suggestion_get_data):
    """
    Tests that SuggestionGetModel raises ValidationError if user_id is missing.
    """
    del base_suggestion_get_data["user_id"]
    with pytest.raises(ValidationError) as exc_info:
        SuggestionGetModel(**base_suggestion_get_data)
    assert "user_id" in str(exc_info.value)


def test_suggestion_get_model_likes_not_int(base_suggestion_get_data):
    """
    Tests that SuggestionGetModel raises ValidationError if likes is not an int.
    """
    base_suggestion_get_data["stars_count"] = "five"
    with pytest.raises(ValidationError) as exc_info:
        SuggestionGetModel(**base_suggestion_get_data)
    assert "stars_count" in str(exc_info.value)


# --- Unit Tests for SuggestionUpdateModel ---


def test_suggestion_update_model_valid_data(base_suggestion_update_data):
    """
    Tests that SuggestionUpdateModel can be successfully instantiated with valid data.
    """
    suggestion_update = SuggestionUpdateModel(**base_suggestion_update_data)

    assert suggestion_update.id == base_suggestion_update_data["id"]
    assert suggestion_update.title == base_suggestion_update_data["title"]
    assert suggestion_update.text_content == base_suggestion_update_data["text_content"]
    assert suggestion_update.article_id == base_suggestion_update_data["article_id"]


def test_suggestion_update_model_invalid_id(base_suggestion_update_data):
    """
    Tests that SuggestionUpdateModel raises ValidationError for invalid ID type.
    """
    base_suggestion_update_data["id"] = "invalid_id"
    with pytest.raises(ValidationError) as exc_info:
        SuggestionUpdateModel(**base_suggestion_update_data)
    assert "id" in str(exc_info.value)
