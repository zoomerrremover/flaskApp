import pytest
from datetime import datetime
from faker import Faker  # Import Faker class
from src import Base, engine
from src.db import User, Course, Article, Suggestion
from src.security.jwt_service import generate_jwt
from src.constants import UserRolesEnum


@pytest.fixture()
def client(app):
    Base.metadata.create_all(engine)
    return app.test_client()


@pytest.fixture
def generate_users():
    def _generate_users(role="user", num_users=1):
        fake = Faker()  # Initialize a Faker instance
        for _ in range(num_users):
            yield {
                "username": fake.user_name(),  # Corrected call
                "password": fake.password(
                    length=12,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True,
                ),
                "date_registered": datetime.utcnow(),
                "email": f"{fake.user_name()}@gmail.com",
                "role": UserRolesEnum(role),
            }

    return _generate_users


@pytest.fixture()
def article_data():
    def _generate_article_data(num_articles=1, user_id=1, course_id=1):
        fake = Faker()
        for _ in range(num_articles):
            yield {
                "title": fake.unique.sentence(nb_words=5),
                "text_content": fake.paragraph(nb_sentences=10),
                "course_id": course_id,
                "user_id": user_id,
                "date_created": datetime.utcnow(),
                "date_posted": None,
            }
    return _generate_article_data


@pytest.fixture
def registered_article(app, registered_user, registered_course, article_data):
    """
    Factory fixture to register a user (optionally with a specific role),
    create a course for that user, then create an article within that course.
    Returns the created article data (including its DB ID), the user data
    (including their access token), and the course data.
    """
    def _registered_article(role="user", num_articles=1):
        course_gen = registered_course()
        course_data, user_data = next(course_gen)
        article_gen = article_data(num_articles, user_data["id"], course_data["id"])
        cache = []
        for _ in range(num_articles):
            article_db_payload = next(article_gen)
            with app.app_context():
                created_article_db = Article(**article_db_payload).save()
                article_db_payload["id"] = created_article_db.id
            cache.append(article_db_payload["id"])
            yield article_db_payload, user_data, course_data
        for entry in cache:
            with app.app_context():
                Article.delete_by_id(entry)
    return _registered_article


@pytest.fixture
def suggestion_data():
    def _generate_suggestion_data(num_suggestions=1, article_id=1):
        fake = Faker()
        for _ in range(num_suggestions):
            yield {
                "title": fake.unique.sentence(nb_words=5)[:32],  # Limit to max_length=32
                "text_content": fake.paragraph(nb_sentences=5)[:8000],  # Limit to max_length=8000
                "article_id": article_id,
            }
    return _generate_suggestion_data


@pytest.fixture
def registered_suggestion(app, registered_article, suggestion_data):
    def _registered_suggestion(num_suggestions=1, user_role="user"):
        article_info, user_data, course_data = next(registered_article(num_articles=1, role=user_role))

        suggestion_gen = suggestion_data(num_suggestions, article_info["id"])
        cache = []
        for _ in range(num_suggestions):
            suggestion_db_payload = next(suggestion_gen)
            addon_data = {
                "user_id": user_data["id"],
                "date_posted": datetime.utcnow(),
            }
            with app.app_context():
                created_suggestion_db = Suggestion(**suggestion_db_payload, **addon_data).save()
                suggestion_db_payload["id"] = created_suggestion_db.id
                suggestion_db_payload["user_id"] = addon_data["user_id"]
                suggestion_db_payload["date_posted"] = addon_data["date_posted"].isoformat()
            cache.append(suggestion_db_payload["id"])
            yield suggestion_db_payload, user_data, article_info, course_data
        for entry in cache:
            with app.app_context():
                Suggestion.delete_by_id(entry)
    return _registered_suggestion


@pytest.fixture()
def registered_user(app, client, generate_users):
    def _generate_registered_users(role="user", num_users=1):
        user_gen = generate_users(role, num_users)
        cache = []
        for _ in range(num_users):
            user_data = next(user_gen)
            with app.app_context():
                editor_user_db = User(**user_data).save()
                user_data["access_token"] = generate_jwt(editor_user_db)
                user_data["id"] = editor_user_db.id
            cache.append(user_data["id"])
            yield user_data
        for entry in cache:
            with app.app_context():
                User.delete_by_id(entry)
    return _generate_registered_users


@pytest.fixture
def course_data():
    """Fixture to generate a single set of fake course data."""
    fake = Faker()
    return {
        "title": fake.unique.sentence(nb_words=5),
        "text_content": fake.paragraph(nb_sentences=10),
        "category": fake.word(),
    }


@pytest.fixture
def generate_course_data():
    """Factory fixture to generate multiple sets of fake course data."""
    def _generate_course_data(num_courses=1, user_id=1):
        fake = Faker()
        for _ in range(num_courses):
            yield {
                "title": fake.unique.sentence(nb_words=5),
                "text_content": fake.paragraph(nb_sentences=10),
                "category": fake.word(),
                "date_created": datetime.utcnow(),
                "user_id": user_id,
            }
    return _generate_course_data


@pytest.fixture
def registered_course(app, client, registered_user, generate_course_data):
    """
    Factory fixture to register a user, then create a course for that user,
    and return the course data and the user's token.
    """
    def _registered_course_and_token(num_courses=1, user_role="user"):
        user_data = next(registered_user(user_role, 1))
        course_gen = generate_course_data(num_courses, user_data["id"])
        cache = []
        for _ in range(num_courses):
            course_data = next(course_gen)
            with app.app_context():
                created_course = Course(**course_data).save()
                course_data["id"] = created_course.id
            cache.append(course_data["id"])
            yield course_data, user_data
        for entry in cache:
            with app.app_context():
                Course.delete_by_id(entry)
    return _registered_course_and_token

