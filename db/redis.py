import os
from typing import Union

from dotenv import load_dotenv
from redis import Redis

from db.cache import AbstractCache

load_dotenv()

REDIS_HOST: str = os.getenv("REDIS_HOST")
REDIS_PORT: int = int(os.getenv("REDIS_PORT"))


class RedisCache(AbstractCache):
    def add_token(self, key: str, expire: int, value: Union[bytes, str]):
        self.cache.setex(name=f"{key}", time=expire, value=f"{value}")

    def delete_token(self, key: str):
        self.cache.delete(f"{key}")

    def is_jti_blacklisted(self, jti) -> bool:
        return bool(self.cache.get(name=jti))

    def save_access_history(self, user_id: str, access_history: str):
        self.cache.lpush(f"{user_id}", access_history)

    def get_access_history(self, user_id: str) -> str:
        return self.cache.lrange(name=f"{user_id}", start=0, end=-1)

    def close(self):
        self.cache.close()


redis_cache: RedisCache = RedisCache(
    cache_instance=Redis(
        host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True, charset="utf-8"
    )
)
