from collections.abc import Sequence
from typing import Any

from psycopg import Cursor


def create_insert_sql(table_name: str, headers: list[str]) -> str:
    """
    建立插入資料的SQL

    Args:
        table_name (str): 表格名稱
        headers (list[str]): 欄位名稱

    Returns:
        str: 插入資料的SQL
    """
    return f"""INSERT INTO {table_name} ({", ".join(headers)}) VALUES ({", ".join(["%s"] * len(headers))});"""


def insert_data(
    cursor: Cursor,
    table_name: str,
    headers: list[str],
    data: Sequence[Any],
) -> None:
    """
    插入資料

    Args:
        cursor (Cursor): 游標物件
        table_name (str): 表格名稱
        headers (list[str]): 欄位名稱
        data (Sequence[Any]): 資料
    """
    sql = create_insert_sql(table_name, headers)
    cursor.execute(sql, data)  # type: ignore


def insert_many_data(
    cursor: Cursor,
    table_name: str,
    headers: list[str],
    data: Sequence[Sequence[Any]],
) -> None:
    """
    插入多筆資料

    Args:
        cursor (Cursor): 游標物件
        table_name (str): 表格名稱
        headers (list[str]): 欄位名稱
        data (Sequence[Sequence[Any]]): 資料
    """
    sql = create_insert_sql(table_name, headers)
    cursor.executemany(sql, data)  # type: ignore
