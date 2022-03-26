import os
from logging import config as logging_config
from pathlib import Path

from dotenv import load_dotenv

from core.logger import LOGGING

env_path = Path(__file__).resolve().parent.parent.parent / "envs/fastapi.env"
load_dotenv(dotenv_path=env_path)

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Версия сервиса
VERSION: str = "0.1.0"

# JWT SETTINGS
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv("PROJECT_NAME", "movies")

# Настройки Redis
REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

# Настройки Elasticsearch
ELASTIC_HOST: str = os.getenv("ELASTIC_HOST", "127.0.0.1")
ELASTIC_PORT: int = int(os.getenv("ELASTIC_PORT", 9200))

CACHE_EXPIRE_IN_SECONDS: int = 60 * 5  # 5 минут

# Корень проекта
BASE_DIR = Path(__file__).resolve().parent.parent
