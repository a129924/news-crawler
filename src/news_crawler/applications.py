from collections.abc import Generator, Iterable

from .parse_company.parse import Company


class Application:
    def __init__(self, db_config: dict[str, str]):
        self.db_config = db_config

    def connect_db(self):
        from .db.connect_db import create_connection

        self.connection = create_connection(
            self.db_config["POSTGRES_DB"],
            self.db_config["POSTGRES_USER"],
            self.db_config["POSTGRES_PASSWORD"],
        )

        return self

    def get_cursor(self):
        from .db.connect_db import get_cursor

        return get_cursor(self.connection)

    def parse_company_data(self, filter_company_name: Iterable[str] = {"上市", "上櫃"}):
        from .parse_company.parse import main

        yield from main(filter_company_name=filter_company_name)

    def process_company_data(self, companys: Generator[Company, None, None]):
        first_company = next(companys)
        headers = list(first_company.keys())
        data = [tuple(first_company.values())] + [
            tuple(company.values()) for company in companys
        ]

        return headers, data

    def insert_company_data(self, table_name: str):
        with self.connect_db().get_cursor() as cursor:
            from .db.execute import insert_many_data

            headers, data = self.process_company_data(
                companys=self.parse_company_data()
            )

            insert_many_data(
                cursor=cursor, table_name=table_name, headers=headers, data=data
            )

    def pipeline(self):
        self.insert_company_data(table_name="company")
