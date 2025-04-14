from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_USER = getenv('DB_USER',default='admin')
DB_PASS = getenv('DB_PASS',default=12345)
DB_HOST = getenv('DB_HOST',default='localhost')
DB_PORT = getenv('DB_PORT',default=5432)
DB_NAME = getenv('DB_NAME',default='default_db')

DB_STRING = (
    f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
)