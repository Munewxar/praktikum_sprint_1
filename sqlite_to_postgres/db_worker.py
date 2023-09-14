import sqlite3
from dataclasses import astuple, fields

import psycopg2
from psycopg2.extensions import connection as _connection

from models import (FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork,
                    TableType)


TABLE_NAME_TO_TYPE = {
    'film_work': FilmWork,
    'genre': Genre,
    'person': Person,
    'genre_film_work': GenreFilmWork,
    'person_film_work': PersonFilmWork
}


class SqlUtilMixin:
    def get_field_names(self, table_type: TableType) -> list[str]:
        """Возвращает список имен полей для заданной таблицы"""
        return [field.name for field in fields(table_type)]


class SQLiteExtractor(SqlUtilMixin):
    BUNCH_SIZE = 500

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def execute_query(self, table_name: str) -> None:
        """Выполняет запрос на получение записей из указанной таблицы"""
        self._set_table_type(table_name)

        query = self._generate_query(table_name)
        self.cursor.execute(query)

    def fetch_records(self) -> list[TableType]:
        """Возвращает следующую пачку записей из таблицы 
        (по умолочанию - 500 записей)
        """
        records = self.cursor.fetchmany(self.BUNCH_SIZE)
        return [self.table_type(**dict(record)) for record in records]

    def _set_table_type(self, table_name: str) -> None:
        """Сохраняет тип таблицы в поле класса"""
        self.table_type = TABLE_NAME_TO_TYPE[table_name]

    def _generate_query(self, table_name: str) -> str:
        """Формирует строку запроса на получение записей из таблицы"""
        field_names = self.get_field_names(self.table_type)

        fields_to_select = ', '.join(field_names)
        query = f'SELECT {fields_to_select} FROM {table_name}'

        return query


class PostgresSaver(SqlUtilMixin):

    def __init__(self, conn: _connection) -> None:
        self.conn = conn
        self.cursor = conn.cursor()

        psycopg2.extras.register_uuid()

    def insert_records(
            self,
            table_name: str,
            records: list[TableType]) -> None:
        """Выполняет запрос на внесение записей в указанную таблицу"""
        query = self._generate_query(table_name, records)
        self.cursor.execute(query)

    def _generate_query(
            self,
            table_name: str,
            records: list[TableType]) -> str:
        """Формирует строку запроса на внесение данных в таблицу"""
        table_type = TABLE_NAME_TO_TYPE[table_name]
        field_names = self.get_field_names(table_type)

        field_count = ', '.join(['%s'] * len(field_names))
        fields_to_insert = ', '.join(field_names)
        values_to_insert = ','.join(
            self.cursor.mogrify(
                f"({field_count})",
                astuple(record)).decode('utf-8') for record in records
        )

        query = (
            f'INSERT INTO content.{table_name} ({fields_to_insert}) '
            f'VALUES {values_to_insert} '
            f'ON CONFLICT (id) DO NOTHING')

        return query
