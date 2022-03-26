import logging
from contextlib import closing
from datetime import datetime

import psycopg2
from config import dsl, es_conf
from elasticsearch_loader import ElasticSearchLoader
from index_schemas import FILM_WORK_INDEX_BODY, GENRE_INDEX_BODY, PERSON_INDEX_BODY
from postgres_loader import PostgresLoader
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from query import film_work_query, genre_query, person_query

from services import backoff

logger = logging.getLogger("LoaderStart")


def load_from_postgres(pg_conn: _connection, state_file: str, query: str) -> list:
    postgres_loader = PostgresLoader(pg_conn, state_file=state_file)
    data = postgres_loader.loader_from_postgresql(query=query)
    return data


@backoff()
def query_postgres(state_file: str, query: str) -> list:
    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        logger.info(
            f"{datetime.now()}\n\nустановлена связь с PostgreSQL. Начинаем загрузку данных"
        )
        load_pq = load_from_postgres(
            pg_conn=pg_conn, state_file=state_file, query=query
        )
    return load_pq


def save_elastic(
    columns: list[str],
    state_file: str,
    query: str,
    index_name: str,
    index_schema: dict,
) -> None:
    """
    Загружаем пачками данные в ElasticSearch, предварительно создаем индекс в бд.
    """
    logger.info(
        f"{datetime.now()}\n\nустановлена связь с ElasticSearch. Начинаем загрузку данных"
    )
    ElasticSearchLoader(host=es_conf, index_name=index_name).create_index(
        index_schema=index_schema
    )
    data_from_postgres = query_postgres(state_file=state_file, query=query)
    count: int = len(data_from_postgres)
    index: int = 0
    actions: list = []
    while count != 0:
        if count >= batch:
            for row in data_from_postgres[index: index + batch]:
                actions.append(dict(zip(columns, row)))
                index += 1
            count -= batch
            ElasticSearchLoader(
                host=es_conf, index_name=index_name
            ).load_data_to_elasticsearch(actions=actions, state_file=state_file)
            actions.clear()
        else:
            ElasticSearchLoader(
                host=es_conf, index_name=index_name
            ).load_data_to_elasticsearch(
                actions=[
                    dict(zip(columns, row))
                    for row in data_from_postgres[index : index + count]
                ],
                state_file=state_file,
            )
            count -= count


if __name__ == "__main__":

    film_work_columns: list[str] = [
        "id",
        "title",
        "description",
        "imdb_rating",
        "permissions",
        "genre",
        "director",
        "actors_names",
        "writers_names",
        "actors",
        "writers",
        "directors",
    ]
    genre_columns: list[str] = ["id", "name"]
    person_columns: list[str] = ["id", "full_name", "roles", "film_ids"]
    batch: int = 50
    """ start elastic savers """
    save_elastic(
        columns=film_work_columns,
        state_file="film_work_data.txt",
        query=film_work_query,
        index_name="movies",
        index_schema=FILM_WORK_INDEX_BODY,
    )
    save_elastic(
        columns=genre_columns,
        state_file="genre_data.txt",
        query=genre_query,
        index_name="genre",
        index_schema=GENRE_INDEX_BODY,
    )
    save_elastic(
        columns=person_columns,
        state_file="person_data.txt",
        query=person_query,
        index_name="person",
        index_schema=PERSON_INDEX_BODY,
    )
