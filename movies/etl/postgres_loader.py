from datetime import datetime

from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from state import JsonFileStorage, State


class PostgresLoader:
    def __init__(self, pg_conn: _connection, state_file: str, state_key="key"):
        self.conn = pg_conn
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        self.key = state_key
        self.state_key = State(JsonFileStorage(file_path=state_file)).get_state(
            state_key
        )
        self.batch: int = 100
        self.data: list = []
        self.count: int = 0

    def get_state_key(self):
        """
        Определяем какую дату будем использовать для сравнения при запросе.
        """
        return self.state_key

    def loader_from_postgresql(self, query: str) -> list:
        """
        Главный запрос на получение данных из бд.
        """
        self.cursor.execute(query % self.get_state_key())
        records = self.cursor.fetchall()
        self.conn.close()
        return records
