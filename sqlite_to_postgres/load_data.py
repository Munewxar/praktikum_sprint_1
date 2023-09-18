import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from contextlib import closing

import logger
from db_worker import TABLE_NAME_TO_TYPE, PostgresSaver, SQLiteExtractor


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_conn: _connection) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    for table in TABLE_NAME_TO_TYPE.keys():
        try:
            sqlite_extractor.execute_query(table)
        except sqlite3.Error as e:
            logger.log_error(str(e))

        logger.log_info(f'Processing {table}')

        has_records = True
        while has_records:
            records = sqlite_extractor.fetch_records()

            if records:
                try:
                    postgres_saver.insert_records(table, records)
                except psycopg2.Error as e:
                    logger.log_error(str(e))
            else:
                has_records = False
                logger.log_info(f'Finish processing {table}')


def run_data_transfer() -> None:
    """Запускает процесс переноса данных из SQLite в Postgresql"""
    dsl = {
        'dbname': 'movies_database',
        'user': 'app',
        'password': '123qwe',
        'host': '127.0.0.1',
        'port': 5432
    }

    with closing(sqlite3.connect('db.sqlite')) as sqlite_conn, \
            closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:

        load_from_sqlite(sqlite_conn, pg_conn)


if __name__ == '__main__':
    run_data_transfer()
