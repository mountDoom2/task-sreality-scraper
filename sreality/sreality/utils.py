import os
import typing

import psycopg2


def connect_db_from_env():
    """Syntax sugar for loading database info from environment and using it for establishing connection."""
    db_info = get_db_info_from_env()
    return connect_db(**db_info)


def close_db(conn, cursor) -> None:
    """Close database connection."""
    conn.close()
    cursor.close()


def connect_db(host: str, user: str, password: str, database: str, port: int):
    """Connect to Postgre database.

    :param host: Database hostname.
    :param user: Database user.
    :param password: Database password.
    :param database: Database name.
    :param port: Database port.
    :return: Postgres database connection and cursor for query execution.
    """
    conn = psycopg2.connect(
        host=host, user=user, password=password, database=database, port=port
    )
    cursor = conn.cursor()

    return conn, cursor


def get_db_info_from_env() -> typing.Dict[str, typing.Union[str, int]]:
    """Load database connection info from environment.

    :return: Database connection info.
    """
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "user": os.getenv("POSTGRES_DATABASE", "postgres"),
        "password": os.getenv("POSTGRES_USER", "postgres"),
        "database": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "port": os.getenv("POSTGRES_PORT", 5432),
    }
