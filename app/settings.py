from os import getenv
from dotenv import load_dotenv
import re

load_dotenv()

DB_USER = getenv('DB_USER', default='admin')
DB_PASS = getenv('DB_PASS', default=12345)
DB_HOST = getenv('DB_HOST', default='localhost')
DB_PORT = getenv('DB_PORT', default=5432)
DB_NAME = getenv('DB_NAME', default='default_db')
DB_STRING =  f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

JWT_KEY = getenv('JWT_KEY', default='SECRET')
ACCESS_TOKEN_TIME = 30
PASSWORD_KEY = getenv('PASSWORD_KEY')
ALGORITHM = 'HS256'
AUTH_HEADER = 'Authorization'

RE_PASSWORD = re.compile("^(?=.*[a-zA-Z])(?!.*\s).+$")
RE_USERNAME = re.compile("^[a-zA-Z0-9_]{3,20}$")
RE_TEXT_CONTENT = re.compile(r"^[a-zA-Z0-9\s.,!?'-]+$")
