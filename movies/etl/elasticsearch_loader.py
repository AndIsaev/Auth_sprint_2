import json
import logging
from datetime import datetime

from elasticsearch import Elasticsearch
from state import JsonFileStorage, State

from services import backoff

logger = logging.getLogger("ESLoader")


class ElasticSearchLoader:
    def __init__(self, host: list, index_name: str, state_key="key"):
        self.client = Elasticsearch(host)
        self.data = []
        self.index_name = index_name
        self.key = state_key

    @backoff()
    def create_index(self, index_schema: dict) -> None:
        """
        Создаем индекс для Elasticsearch.
        """
        index = self.index_name
        exist = self.client.indices.exists(index=index)
        if not exist:
            result = self.client.indices.create(
                index=index, ignore=400, body=index_schema
            )
            if result.get("status") == 200:
                logger.info(f"\nиндекс {index} создан\t{datetime.now()}\n")
            else:
                logger.info(
                    f"\nиндекс {index} создан не был, ошибка 400\t{datetime.now()}\n"
                )
        else:
            logger.warning(f"\nиндекс {index} был создан ранее\t{datetime.now()}\n")

    @backoff()
    def bulk_data_to_elasticsearch(self) -> None:
        self.client.bulk(index=self.index_name, body=self.data, refresh=True)

    def load_data_to_elasticsearch(self, actions: list, state_file: str) -> None:
        """
        Загружаем данные пачками в Elasticsearch предварительно присваивая записям id.
        """
        data_json = json.dumps(actions)
        load_json = json.loads(data_json)
        for row in load_json:
            self.data.append({"create": {"_index": self.index_name, "_id": row["id"]}})
            self.data.append(row)
            self.bulk_data_to_elasticsearch()
            self.data.clear()
        State(storage=JsonFileStorage(file_path=state_file)).set_state(
            key=f"{self.key}", value=f"{datetime.now()}"
        )
