import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    FLASK_HOST: str = os.getenv("FLASK_HOST")
    FLASK_PORT: int = int(os.getenv("FLASK_PORT"))
    SERVICE_URL: str = f"http://{FLASK_HOST}:{FLASK_PORT}"
    # REDIS
    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT"))
