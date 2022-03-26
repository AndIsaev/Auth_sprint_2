from .schema_template import TEMPLATE_INDEX_BODY

FILM_WORK_INDEX_BODY: dict = {
    **TEMPLATE_INDEX_BODY,
    "mappings": {
        "dynamic": "strict",
        "properties": {
            "id": {"type": "keyword"},
            "title": {
                "type": "text",
                "analyzer": "ru_en",
                "fields": {"raw": {"type": "keyword"}},
            },
            "description": {"type": "text", "analyzer": "ru_en"},
            "imdb_rating": {"type": "float"},
            "permissions": {"type": "text", "analyzer": "ru_en"},
            "genre": {"type": "text", "analyzer": "ru_en"},
            "director": {"type": "text", "analyzer": "ru_en"},
            "actors_names": {"type": "text", "analyzer": "ru_en"},
            "writers_names": {"type": "text", "analyzer": "ru_en"},
            "actors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "writers": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
            "directors": {
                "type": "nested",
                "dynamic": "strict",
                "properties": {
                    "id": {"type": "keyword"},
                    "full_name": {"type": "text", "analyzer": "ru_en"},
                },
            },
        },
    },
}
