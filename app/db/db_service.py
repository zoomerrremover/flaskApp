from operator import truediv

from app.db.models import User, Post
from datetime import datetime

def create_user(
    username:str,
    password:str,
    role:str = 'user'
) -> User:
    return User(
        username=username,
        password = password,
        role = role
    ).save().as_dict()

def get_users():
    return User.get_users()

def get_user_by_id(user_id:int):
    return User.get_user_by_id(user_id)

def delete_user_by_id(user_id:int):
    return User.delete_user_by_id(user_id)

def update_user_by_id(user_id:int, **kwargs):
    return User.update_user_by_id(user_id,**kwargs)

def create_post(title:str,text_content:str,date_posted:datetime,author:int) -> Post:
    return Post(
        title=title,
        text_content=text_content,
        date_posted=date_posted,
        author=User.get_user_by_id(author)
    )

def get_posts():
    return Post.get_posts()

def update_post_by_id(post_id:int):
    return Post.update_post_by_id(post_id)

def delete_post_by_id(post_id:int):
    return Post.delete_post_by_id(post_id)

def search_post_by_text_content(search_q:str):
    def search_alg(input:str)->bool:
        """
        TODO:
        Implement actual algorythm here
        Use closure to secure that search_q
        Compare them using either library , or self made algorythm.
        """
        return True
    return Post.search_posts_by_content(search_alg)
