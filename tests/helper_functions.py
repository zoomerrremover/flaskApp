import random
from datetime import datetime, timezone

from faker import Faker

from src.constants import UserRolesEnum
from src.db import Article, Course, Suggestion, User

fake = Faker()


def generate_user_data(role: str = "user") -> User:
    return User(
        **{
            "id": random.randint(1, 99),
            "username": fake.user_name(),  # Corrected call
            "password": fake.password(
                length=12,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
            "date_registered": datetime.now(timezone.utc),
            "email": f"{fake.user_name()}@gmail.com",
            "role": UserRolesEnum(role),
        }
    )


def generate_course_data(user_id: int = 1) -> Course:
    return Course(
        **{
            "id": random.randint(1, 99),
            "title": fake.unique.sentence(nb_words=5),
            "text_content": fake.paragraph(nb_sentences=10),
            "category": fake.word(),
            "date_created": datetime.now(timezone.utc),
            "user_id": user_id,
        }
    )


def generate_article_data(course_id: int = 1, user_id: int = 1) -> Article:
    return Article(
        **{
            "id": random.randint(1, 99),
            "title": fake.unique.sentence(nb_words=5),
            "text_content": fake.paragraph(nb_sentences=10),
            "course_id": course_id,
            "user_id": user_id,
            "date_created": datetime.now(timezone.utc),
            "date_posted": None,
        }
    )


def generate_suggestion_data(article_id: int = 1, user_id: int = 1) -> Suggestion:
    return Suggestion(
        **{
            "id": random.randint(1, 99),
            "title": fake.unique.sentence(nb_words=5)[:32],
            "text_content": fake.paragraph(nb_sentences=5)[:8000],
            "article_id": article_id,
            "user_id": user_id,
            "date_posted": datetime.now(timezone.utc),
        }
    )
