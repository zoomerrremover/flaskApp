import pytest
from src import app as application
from datetime import datetime


@pytest.fixture()
def app():
    return application


@pytest.fixture()
def mock_db_session(mocker):
    return mocker.patch("src.db.models.common.session", autospec=True)


@pytest.fixture
def base_article_create_data():
    """
    Provides a dictionary with valid data for ArticleCreateModel.
    """
    return {
        "title": "My Awesome Article",
        "text_content": "This is some content for my article.",
        "course_id": 101,
    }


@pytest.fixture
def base_article_get_data(base_article_create_data):
    """
    Provides a dictionary with valid data for ArticleGetModel,
    building upon base_article_create_data.
    """
    data = base_article_create_data.copy()
    data.update({"id": 1, "user_id": 5, "date_posted": datetime.utcnow()})
    return data


@pytest.fixture
def base_article_update_data(base_article_create_data):
    """
    Provides a dictionary with valid data for ArticleUpdateModel,
    building upon base_article_create_data.
    """
    data = base_article_create_data.copy()
    data.update({"id": 10})
    return data


@pytest.fixture
def base_course_create_data():
    """
    Provides a dictionary with valid data for CourseCreateModel.
    """
    return {
        "title": "Introduction to Python",
        "text_content": "This course covers the basics of Python programming, from variables to functions.",
        "category": "Programming",
    }


@pytest.fixture
def base_course_get_data(base_course_create_data):
    """
    Provides a dictionary with valid data for CourseGetModel,
    building upon base_course_create_data.
    """
    data = base_course_create_data.copy()
    data.update({"id": 1, "user_id": 101, "date_posted": datetime.now()})
    return data


@pytest.fixture
def base_course_update_data(base_course_create_data):
    """
    Provides a dictionary with valid data for CourseUpdateModel,
    building upon base_course_create_data.
    """
    data = base_course_create_data.copy()
    data.update({"id": 2})
    return data


@pytest.fixture
def valid_username_data():
    """Provides a dictionary with a valid username."""
    return {"username": "test_user123"}


@pytest.fixture
def valid_role_data():
    """Provides a dictionary with a valid role."""
    return {"role": "user"}


@pytest.fixture
def valid_password_data():
    """Provides a dictionary with a valid password."""
    return {"password": "StrongPass123!"}


@pytest.fixture
def valid_email_data():
    """Provides a dictionary with a valid email."""
    return {"email": "test@example.com"}


@pytest.fixture
def base_user_get_data(valid_username_data, valid_role_data):
    """Provides valid data for UserGetModel."""
    data = {"id": 1, "date_registered": datetime.now()}
    data.update(valid_username_data)
    data.update(valid_role_data)
    return data


@pytest.fixture
def base_user_admin_get_data(base_user_get_data, valid_email_data):
    """Provides valid data for UserAdminGetModel."""
    data = base_user_get_data.copy()
    data.update(valid_email_data)
    return data


@pytest.fixture
def base_user_login_data(valid_username_data, valid_password_data):
    """Provides valid data for UserLogInModel."""
    data = valid_username_data.copy()
    data.update(valid_password_data)
    return data


@pytest.fixture
def base_user_role_update_data(valid_role_data):
    """Provides valid data for UserRoleUpdateModel."""
    data = {"id": 5}
    data.update(valid_role_data)
    return data


@pytest.fixture
def base_user_update_data(valid_username_data, valid_password_data, valid_email_data):
    """Provides valid data for UserUpdateModel."""
    data = valid_username_data.copy()
    data.update(valid_password_data)
    data.update(valid_email_data)
    return data


@pytest.fixture
def base_suggestion_create_data():
    """
    Provides a dictionary with valid data for SuggestionCreateModel.
    """
    return {
        "title": "Improve Section 3",
        "text_content": "The explanation in section 3 could be clearer with an additional example.",
        "article_id": 10,
    }


@pytest.fixture
def base_suggestion_get_data(base_suggestion_create_data):
    """
    Provides a dictionary with valid data for SuggestionGetModel,
    building upon base_suggestion_create_data.
    """
    data = base_suggestion_create_data.copy()
    data.update(
        {
            "id": 1,
            "user_id": 101,
            "date_posted": datetime.now(),
            "stars_count": 1,
        }
    )
    return data


@pytest.fixture
def base_suggestion_update_data(base_suggestion_create_data):
    """
    Provides a dictionary with valid data for SuggestionUpdateModel,
    building upon base_suggestion_create_data.
    """
    data = base_suggestion_create_data.copy()
    data.update({"id": 2})
    return data


@pytest.fixture
def base_suggestion_reaction_data():
    """
    Provides a dictionary with valid data for SuggestionReactionModel.
    """
    return {"id": 3, "star": True}
