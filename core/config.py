import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY")
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
JWT_BLACKLIST_ENABLED: bool = True
JWT_COOKIE_SECURE: bool = False
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
TESTING: bool = os.getenv("TESTING") == "True"

# Корень проекта
BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
