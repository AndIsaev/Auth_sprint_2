import os

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from core import config

load_dotenv()

DB_USER: str = os.getenv("DB_USER")
DB_PASS: str = os.getenv("DB_PASS")
DB_HOST: str = os.getenv("DB_HOST")
DB_PORT: int = int(os.getenv("DB_PORT"))


if config.TESTING:
    """test db"""
    DB_TEST_NAME: str = os.getenv("DB_TEST_NAME")
    psql_db_url: str = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_TEST_NAME}"
    )
    psql_db = SQLAlchemy()
else:
    """prod db"""
    DB_NAME: str = os.getenv("DB_NAME")
    psql_db_url: str = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    psql_db = SQLAlchemy()
