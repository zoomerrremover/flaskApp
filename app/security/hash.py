from passlib.context import CryptContext
from app.settings import PASSWORD_KEY

password_contex = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_salt_password(password: str) -> str:
    return PASSWORD_KEY + password


def verify_password(password: str, hashed_password: str):
    return password_contex.verify(get_salt_password(password), hashed_password)


def passwd_to_hash(password: str) -> str:
    return password_contex.hash(get_salt_password(password))
