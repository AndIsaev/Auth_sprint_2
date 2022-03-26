import logging
import os
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / "envs/etl.env"
load_dotenv(dotenv_path=env_path)

logging.basicConfig(filename="logs/etl.log", level="INFO")
logger = logging.getLogger()
logger.setLevel(level="INFO")

dsl = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.environ.get("DB_HOST"),
    "port": os.environ.get("DB_PORT"),
}

es_conf = [
    {
        "host": os.getenv("ES_HOST"),
        "port": os.getenv("ES_PORT"),
    }
]
