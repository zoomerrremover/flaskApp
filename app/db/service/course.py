from app.db.models.concrete import Course
from app.db.service.common import TextContentDbService


class CourseDbService(TextContentDbService):
    MODEL = Course

    @classmethod
    def get_by_category(cls, category: str, limit: int):
        cls.MODEL.search_by_category(limit, category)
