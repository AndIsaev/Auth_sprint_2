import abc
import datetime
import json
import logging
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        if not self.file_path:
            return

        with open(self.file_path, "w") as f:
            json.dump(state, f)

    def retrieve_state(self) -> Optional[dict]:
        if self.file_path:
            logging.info("Не установлен путь до файла.")
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
                if data:
                    return data
        except FileNotFoundError:
            self.save_state({})


class State:
    def __init__(self, storage: BaseStorage):
        self.storage = storage
        self.state = self.retrieve_state()

    def retrieve_state(self) -> dict:
        return self.storage.retrieve_state() or {}

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        self.state[key] = value
        self.storage.save_state(self.state)

    def get_state(self, key: str) -> Any:
        """Получить состояние по определённому ключу"""
        return self.state.get(key) or datetime.datetime.min
