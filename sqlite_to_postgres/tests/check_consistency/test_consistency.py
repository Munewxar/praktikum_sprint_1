import pytest

import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from dataclasses import fields

import sys
sys.path.append('../../')


from models import (FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork,
                    TableType)
from db_worker import TABLE_NAME_TO_TYPE


DSL = {
    'dbname': 'movies_database',
    'user': 'app',
    'password': '123qwe',
    'host': '127.0.0.1',
    'port': 5432
}

POSTGRES_SCHEMA = 'content'


def test_records_amount_equals():
    with sqlite3.connect('../../db.sqlite') as sqlite_conn, \
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:

        for table in TABLE_NAME_TO_TYPE.keys():
            sqlite_records_amount = _get_records_amount(sqlite_conn, table)
            postgres_records_amount = _get_records_amount(
                pg_conn, table, POSTGRES_SCHEMA)

            assert sqlite_records_amount == postgres_records_amount, \
                'Should have the same records amount'


def test_data_equals():
    with sqlite3.connect('../../db.sqlite') as sqlite_conn, \
            psycopg2.connect(**DSL, cursor_factory=DictCursor) as pg_conn:

        for table in TABLE_NAME_TO_TYPE.keys():
            sqlite_records = _fetch_records(sqlite_conn, table)
            postgres_records = _fetch_records(pg_conn, table, POSTGRES_SCHEMA)

            assert sorted(sqlite_records, key=lambda x: x.id) == sorted(
                postgres_records, key=lambda x: x.id), 'Should have the same data'


def _get_records_amount(conn, table, schema=None):
    cursor = conn.cursor()

    query = _generate_query_for_records_amount(table, schema)
    cursor.execute(query)

    return cursor.fetchone()[0]


def _generate_query_for_records_amount(table, schema=None):
    if schema:
        return f'SELECT count(id) FROM {schema}.{table}'
    else:
        return f'SELECT count(id) FROM {table}'


def _fetch_records(conn, table_name, schema=None):
    if isinstance(conn, sqlite3.Connection):
        conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    query = _generate_query_for_records(table_name, schema)
    cursor.execute(query)

    records = cursor.fetchall()
    table_type = TABLE_NAME_TO_TYPE[table_name]

    return [table_type(**dict(record)) for record in records]


def _generate_query_for_records(table_name, schema=None):
    field_names = _get_field_names(table_name)
    fields_to_select = ', '.join(field_names)

    if schema:
        return f'SELECT {fields_to_select} FROM {schema}.{table_name}'
    else:
        return f'SELECT {fields_to_select} FROM {table_name}'


def _get_field_names(table_name):
    table_type = TABLE_NAME_TO_TYPE[table_name]
    return [field.name for field in fields(table_type)]
