import pytest
from datetime import datetime
from faker import Faker  # Import Faker class
from http import HTTPStatus
from src import Base, engine
from src.db import User, Course
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
def registered_user(app, client, generate_users):
    def _generate_registered_users(role="user", num_users=1):
        user_gen = generate_users(role, num_users)
        for _ in range(num_users):
            user_data = next(user_gen)
            with app.app_context():
                editor_user_db = User(**user_data).save()
                user_data["access_token"] = generate_jwt(editor_user_db)
                user_data["id"] = editor_user_db.id
            yield user_data
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
        for _ in range(num_courses):
            course_data = next(course_gen)
            with app.app_context():
                created_course = Course(**course_data).save()
                course_data["id"] = created_course.id
            yield course_data, user_data
    return _registered_course_and_token

