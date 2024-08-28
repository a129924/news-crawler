from collections.abc import Generator, Iterable
from contextlib import AbstractContextManager

from psycopg import Cursor
from typing_extensions import Self

from .parse_company.parse import Company


class Application:
    def __init__(self, db_config: dict[str, str]):
        self.db_config = db_config

    def connect_db(self) -> Self:
        """
        connect_db

        Returns:
            Self: self
        """
        from .db.connect_db import create_connection

        self.connection = create_connection(
            self.db_config["POSTGRES_DB"],
            self.db_config["POSTGRES_USER"],
            self.db_config["POSTGRES_PASSWORD"],
        )

        return self

    def get_cursor(self) -> AbstractContextManager[Cursor]:
        """
        get_cursor

        Returns:
            ContextManager[Cursor]: cursor
        """
        from .db.connect_db import get_cursor

        return get_cursor(self.connection)

    def parse_company_data(
        self, filter_company_name: Iterable[str] = {"上市", "上櫃"}
    ) -> Generator[Company, None, None]:
        """
        parse_company_data

        Args:
            filter_company_name (Iterable[str], optional): filter_company_name. Defaults to {"上市", "上櫃"}.

        Returns:
            Generator[Company, None, None]: company data
        """
        from .parse_company.parse import main

        yield from main(filter_company_name=filter_company_name)

    def process_company_data(
        self, companys: Generator[Company, None, None]
    ) -> tuple[list[str], list[tuple[str, ...]]]:
        """
        process_company_data

        Args:
            companys (Generator[Company, None, None]): company data

        Returns:
            tuple[list[str], list[tuple[str, ...]]]: headers, data
        """
        first_company = next(companys)

        headers = list(first_company.keys())
        data = [tuple(first_company.values())] + [
            tuple(company.values()) for company in companys
        ]

        return headers, data  # type: ignore

    def insert_company_data(self, table_name: str):
        """
        insert_company_data

        Args:
            table_name (str): table_name
        """
        with self.connect_db().get_cursor() as cursor:
            from .db.execute import insert_many_data

            headers, data = self.process_company_data(
                companys=self.parse_company_data()
            )

            insert_many_data(
                cursor=cursor, table_name=table_name, headers=headers, data=data
            )

    def pipeline(self):
        """
        pipeline
        """
        self.insert_company_data(table_name="company")
