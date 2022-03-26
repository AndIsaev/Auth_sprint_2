import hashlib
from typing import Optional
from pydantic import parse_obj_as

from services.mixins import Schemas


def get_params_films_to_elastic(
    permissions: list[str], page_size: int = 10, page: int = 1, genre: str = None, query: str = None
) -> dict:
    """
    :param permissions: права пользователя в виде ролей
    :param page: номер страницы
    :param page_size: кол-во элементов в ответе
    :param genre: фильтрует фильмы по жанру
    :param query: находит фильмы по полю title
    :return: возвращает правильный body для поиска в Elasticsearch
    """
    films_search: Optional[dict] = {"fuzzy": {"genre": {"value": genre}}} if genre else None
    # query from user
    if query:
        match_value: dict = {"match": {"title": {"query": query, "fuzziness": "auto"}}}
    else:
        match_value: dict = {"match_all": {}}
    # combine body
    body: dict = {
        "size": page_size,
        "from": (page - 1) * page_size,
        "query": {
            "bool": {
                "must": [
                    {"match": {"permissions": {"query": ",".join(permissions), "fuzziness": "auto"}}},
                    {**match_value}
                ],
                "filter": films_search,
            }
        },
    }
    return body


def get_hits(docs: Optional[dict], schema: Schemas):
    hits: dict = docs.get("hits").get("hits")
    data: list = [row.get("_source") for row in hits]
    parse_data = parse_obj_as(list[schema], data)
    return parse_data


def create_hash_key(index: str, params: str) -> str:
    """
    :param index: индекс в elasticsearch
    :param params: параметры запроса
    :return: хешированый ключ в md5
    """
    hash_key = hashlib.md5(params.encode()).hexdigest()
    return f"{index}:{hash_key}"
