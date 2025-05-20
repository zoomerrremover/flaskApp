from app.db.models.models import Course
import datetime

def create_course(title: str, text_content: str, date_posted: datetime, user_id: int, category: str):
    return (
        Course(
            title=title,
            text_content=text_content,
            date_posted=date_posted,
            user_id=user_id,
            category=category
        ).save()
    )


def get_course_by_id(course_id: int):
    return Course.get_by_id(course_id)


def update_course_by_id(course_id: int, **kwargs) -> int:
    return Course.update_by_id(course_id, **kwargs)


def delete_course_by_id(course_id: int) -> None:
    return Course.delete_by_id(course_id)
