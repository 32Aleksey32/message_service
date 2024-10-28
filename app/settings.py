import os

from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base

load_dotenv()

Base = declarative_base()

DATABASE_URL = os.getenv(
    'DATABASE_URL',
    default='postgresql+asyncpg://postgres:postgres@db:5432/message_service'
)
SECRET_KEY = os.getenv('SECRET_KEY', default='secret_key')
ALGORITHM = os.getenv('ALGORITHM', default="HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', default=60))
REDIS_BROKER_URL = os.getenv('REDIS_BROKER_URL', default='redis://redis:6379/0')
BOT_TOKEN = os.getenv('BOT_TOKEN')
