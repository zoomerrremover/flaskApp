from app.db.models.concrete import Course
from app.db.service.common import DbService


class CourseDbService(DbService):
    MODEL = Course
