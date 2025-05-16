from app.db.models import Course
import datetime

def create_course(title: str, text_content: str, date_posted: datetime, user_id: int, category: str):
    return \
        (
            Course(title=title, text_content=text_content, date_posted=date_posted, user_id=user_id, category=category)
            .save()
        )


def search_course_by_author(user_id: int):
    return Course.search_by_user(user_id)


def search_course_by_date(start_date: datetime, end_date: datetime):
    return Course.search_within_date_range(start_date, end_date)


def search_course_by_category(category: str):
    return Course.search_by_category(category)


def search_course_by_inner_content(content: str):
    return Course.search_by_content(content)


def get_course_by_id(course_id: int):
    return Course.get_by_id(course_id)


def update_course_by_id(course_id: int, **kwargs) -> int:
    return Course.update_by_id(course_id, **kwargs)


def delete_course_by_id(course_id: int) -> None:
    return Course.delete_by_id(course_id)
