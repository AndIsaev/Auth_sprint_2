from abc import ABC, abstractmethod
from typing import Union


class AbstractCache(ABC):
    def __init__(self, cache_instance):
        self.cache = cache_instance

    @abstractmethod
    def add_token(self, key: str, expire: int, value: Union[bytes, str]):
        pass

    @abstractmethod
    def delete_token(self, key: str):
        pass

    @abstractmethod
    async def is_jti_blacklisted(self, jti):
        pass

    @abstractmethod
    def save_access_history(self, user_id: str, access_history: str):
        pass

    @abstractmethod
    def get_access_history(self, user_id: str):
        pass

    @abstractmethod
    async def close(self):
        pass
