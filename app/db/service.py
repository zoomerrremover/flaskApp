from app.security.hash import verify_password
from app.db.models import User, Course, Article, Suggestion
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus
from flask import Response
from app.settings import ERR_USERNAME_ORIGINAL
from app.models.user import UserRead, UserSuRead
from app.strategies import string_compare
from app.security.hash import passwd_to_hash

def create_user(
    username:str,
    password:str,
    email: str,
    role:str = 'user'
) -> User:
        return User(
            username=username,
            password = passwd_to_hash(password),
            email = email,
            role = role
        ).save().as_dict()

def get_users():
    users =  User.get_users()
    return [UserRead(username = data.username) for data in users]

def get_users_by_name(name:str):
    users = User.get_filtered_users(string_compare(name))
    return [UserRead(username = data.username) for data in users]

def get_user_by_id(user_id:int):
    data = User.get_user_by_id(user_id)
    return UserRead(username = data.username)

def get_user_login(username:str,password:str):
    comp = string_compare(username)
    predicate =  User.__table__.c.username == username
    user = User.get_filtered_first(predicate)
    result = None
    if user and verify_password(password,user.password):
        result = user
    return result

def get_username_is_original(username:str)->bool:
    predicate = User.__table__.c.username == username
    user = User.get_filtered_user(predicate)
    result = True
    if user:
        result = False
    return result

def get_email_is_valid(email:str)->bool:
    predicate = User.__table__.c.email == email
    user = User.get_filtered_user(predicate)
    result = False
    if not user and is_valid_email(email):
        result = True
    return result

def get_su_user_by_id(user_id:int):
    data = User.get_user_by_id(user_id)
    return UserSuRead(username = data.username, email = data.email)

def delete_user_by_id(user_id:int):
    return User.delete_user_by_id(user_id)

def update_user_by_id(user_id:int, **kwargs):
    return User.update_user_by_id(user_id,**kwargs)

def create_course(
        title:str,
        intro_text:str,
        category:str,
        date_posted:datetime = datetime.now()) -> Course:
    return Course(
        title=title,
        category=category,
        intro_text = intro_text,
        date_posted=date_posted
    )

def get_courses():
    return Course.get_course()

def get_course_by_id(course_id:int):
    return Course.get_course_by_id(course_id)

def update_course_by_id(course_id:int):
    return Course.update_course_by_id(course_id)

def delete_post_by_id(course_id:int):
    return Course.delete_course_by_id(course_id)


def create_article(
        title:str,
        text_content:str,
        course_id:int,
        user_id: int,
        date_posted:datetime = datetime.now()) -> Article:
    return Article(
        title=title,
        text_content = text_content,
        course_id = course_id,
        user_id = user_id,
        date_posted=date_posted
    )

def get_articles():
    return Article.get_articles()

def get_article_by_id(article_id:int):
    return Article.get_article_by_id(article_id)

def update_article_by_id(article_id:int):
    return Article.update_articles_by_id(article_id)

def delete_article_by_id(article_id:int):
    return Article.delete_articles_by_id(article_id)

def create_suggestion(
        title:str,
        text_content:str,
        article_id:int,
        user_id:int,
        up_vote:int = 0,
        down_vote:int = 0,
        date_posted:datetime = datetime.now()) -> Suggestion:
    return Suggestion(
        title=title,
        text_content=text_content,
        article_id = article_id,
        user_id = user_id,
        up_vote = up_vote,
        down_vote = down_vote,
        date_posted=date_posted
    )

def get_suggestions():
    return Suggestion.get_suggestions()

def update_suggestion_by_id(suggestion_id:int):
    return Suggestion.update_post_by_id(suggestion_id)

def delete_suggestion_by_id(suggestion_id:int):
    return Suggestion.delete_suggestion_by_id(suggestion_id)


