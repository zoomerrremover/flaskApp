import pytest
from pydantic import ValidationError
from src.models import CourseCreateModel, CourseGetModel, CourseUpdateModel
from src.exceptions import InvalidDataError
from src.constants import ErrorsMsgEnum


def test_course_create_model_valid_data(base_course_create_data):
    course = CourseCreateModel(**base_course_create_data)
    assert course.title == "Introduction to Python"
    assert (
        course.text_content
        == "This course covers the basics of Python programming,\
        from variables to functions."
    )
    assert course.category == "Programming"


def test_course_create_model_title_too_long(base_course_create_data):
    invalid_data = base_course_create_data.copy()
    invalid_data["title"] = "A" * 999
    with pytest.raises(ValidationError) as exc_info:
        CourseCreateModel(**invalid_data)
    assert "title" in str(exc_info.value)


def test_course_create_model_text_content_too_long(base_course_create_data):
    invalid_data = base_course_create_data.copy()
    invalid_data["text_content"] = "A" * 8001  # Exceeds max_length of 8000
    with pytest.raises(ValidationError) as exc_info:
        CourseCreateModel(**invalid_data)
    assert "text_content" in str(exc_info.value)


def test_course_create_model_category_too_long(base_course_create_data):
    invalid_data = base_course_create_data.copy()
    invalid_data["category"] = "A" * 25  # Exceeds max_length of 24
    with pytest.raises(ValidationError) as exc_info:
        CourseCreateModel(**invalid_data)
    assert "category" in str(exc_info.value)


def test_course_create_model_invalid_title_content(base_course_create_data):
    invalid_data = base_course_create_data.copy()
    invalid_data["title"] = "Title with <bad> chars"
    with pytest.raises(InvalidDataError) as exc_info:
        CourseCreateModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_TEXT_CONTENT in str(exc_info.value)


def test_course_create_model_invalid_text_content(base_course_create_data):
    invalid_data = base_course_create_data.copy()
    invalid_data["text_content"] = "SQL INJECTION: DROP TABLE users;"
    with pytest.raises(InvalidDataError) as exc_info:
        CourseCreateModel(**invalid_data)
    assert ErrorsMsgEnum.ERROR_TEXT_CONTENT in str(exc_info.value)
# --- Unit Tests for CourseGetModel ---


def test_course_get_model_valid_data(base_course_get_data):
    course_get = CourseGetModel(**base_course_get_data)
    assert course_get.id == base_course_get_data["id"]
    assert course_get.title == base_course_get_data["title"]
    assert course_get.text_content == base_course_get_data["text_content"]
    assert course_get.category == base_course_get_data["category"]
    assert course_get.user_id == base_course_get_data["user_id"]
    assert course_get.date_posted == base_course_get_data["date_posted"]
    # Test with date_posted as None
    data_no_date = base_course_get_data.copy()
    data_no_date["date_posted"] = None
    course_get_no_date = CourseGetModel(**data_no_date)
    assert course_get_no_date.date_posted is None


def test_course_get_model_invalid_id(base_course_get_data):
    invalid_data = base_course_get_data.copy()
    invalid_data["id"] = "not_an_int"
    with pytest.raises(ValidationError) as exc_info:
        CourseGetModel(**invalid_data)
    assert "id" in str(exc_info.value)


def test_course_get_model_missing_user_id(base_course_get_data):
    invalid_data = base_course_get_data.copy()
    del invalid_data["user_id"]
    with pytest.raises(ValidationError) as exc_info:
        CourseGetModel(**invalid_data)
    assert "user_id" in str(exc_info.value)
# --- Unit Tests for CourseUpdateModel ---


def test_course_update_model_valid_data(base_course_update_data):
    course_update = CourseUpdateModel(**base_course_update_data)
    assert course_update.id == base_course_update_data["id"]
    assert course_update.title == base_course_update_data["title"]
    assert course_update.text_content == base_course_update_data[
        "text_content"
    ]
    assert course_update.category == base_course_update_data["category"]


def test_course_update_model_invalid_id(base_course_update_data):
    invalid_data = base_course_update_data.copy()
    invalid_data["id"] = [1, 2]  # Invalid ID type
    with pytest.raises(ValidationError) as exc_info:
        CourseUpdateModel(**invalid_data)
    assert "id" in str(exc_info.value)
