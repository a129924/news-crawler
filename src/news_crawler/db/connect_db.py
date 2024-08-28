from collections.abc import Generator
from contextlib import contextmanager

from psycopg import Connection, Cursor


def create_connection(
    db_name: str, user: str, password: str, host: str = "localhost", port: str = "5432"
) -> Connection:
    """
    建立連線

    Args:
        db_name (str): db的名稱
        user (str): 使用者名稱
        password (str): 密碼
        host (str, optional): 主機名稱. Defaults to "localhost".
        port (str, optional): 埠號. Defaults to "5432".

    Returns:
        Connection: 連線物件
    """
    from psycopg import connect

    return connect(
        f"dbname={db_name} user={user} password={password} host={host} port={port}"
    )


@contextmanager
def get_cursor(connection: Connection) -> Generator[Cursor, None, None]:
    """
    取得游標

    Args:
        connection (Connection): 連線物件

    Yields:
        Generator[Cursor, None, None]: 游標物件
    """
    try:
        cur = connection.cursor()
        cur.execute("SET NAMES 'utf8';")

        yield cur

        # connection.commit()

    except Exception as e:
        connection.rollback()

        raise e

    finally:
        cur.close()
        connection.close()
