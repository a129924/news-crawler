from dotenv import dotenv_values


def test_connection():
    from src.news_crawler.connect_db.connect_db import create_connection

    config = dotenv_values("./env/db_config.env")
    connection = create_connection(
        config["POSTGRES_DB"],  # type: ignore
        config["POSTGRES_USER"],  # type: ignore
        config["POSTGRES_PASSWORD"],  # type: ignore
    )
    assert connection is not None


def test_insert_data():
    from src.news_crawler.connect_db.connect_db import (
        create_connection,
        get_cursor,
        insert_data,
    )

    config = dotenv_values("./env/db_config.env")

    connection = create_connection(
        config["POSTGRES_DB"],  # type: ignore
        config["POSTGRES_USER"],  # type: ignore
        config["POSTGRES_PASSWORD"],  # type: ignore
    )
    with get_cursor(connection) as cursor:
        insert_data(
            cursor,
            "test_company",
            ["name", "english_name", "short_name", "market", "code"],
            ("test", "test", "test", "上市", "test"),
        )

        cursor.execute(
            "SELECT name, english_name, short_name, market, code FROM test_company"
        )
        assert cursor.fetchall() == [("test", "test", "test", "上市", "test")]


def test_insert_many_data():
    from src.news_crawler.connect_db.connect_db import (
        create_connection,
        get_cursor,
        insert_many_data,
    )

    config = dotenv_values("./env/db_config.env")

    connection = create_connection(
        config["POSTGRES_DB"],  # type: ignore
        config["POSTGRES_USER"],  # type: ignore
        config["POSTGRES_PASSWORD"],  # type: ignore
    )
    with get_cursor(connection) as cursor:
        insert_many_data(
            cursor,
            "test_company",
            ["name", "english_name", "short_name", "market", "code"],
            [
                ("test", "test", "test", "上市", "test"),
                ("test2", "test2", "test2", "上市", "test2"),
            ],
        )
        cursor.execute(
            "SELECT name, english_name, short_name, market, code FROM test_company"
        )
        assert cursor.fetchall() == [
            ("test", "test", "test", "上市", "test"),
            ("test2", "test2", "test2", "上市", "test2"),
        ]
