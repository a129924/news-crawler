from dotenv import dotenv_values
from scrapy import Spider
from typing_extensions import override

from ..db.execute import insert_data
from ..items import NewsItem
from .base import BasePipeline

__all__ = ["DBItemPipeline"]


class DBItemPipeline(BasePipeline):
    @override
    def open_spider(self, spider) -> None:
        """
        Open the spider and connect to the database.
        """
        from ..db.connect_db import create_connection

        config = dotenv_values("./env/db_config.env")

        self.connection = create_connection(
            config["POSTGRES_DB"],  # type: ignore
            config["POSTGRES_USER"],  # type: ignore
            config["POSTGRES_PASSWORD"],  # type: ignore
        )
        self.cursor = self.connection.cursor()

    @override
    def process_item(self, item: NewsItem, spider: Spider) -> NewsItem:
        """
        Process the item and insert it into the database.

        Args:
            item (NewsItem): The item to be processed.
            spider (Spider): The spider that is processing the item.

        Returns:
            NewsItem: The processed item.

        Raises:
            DropItem: If the item is not valid or an error occurs.
        """
        try:
            insert_data(
                self.cursor,
                table_name="news",
                headers=list(item.keys()),
                data=list(item.values()),
            )

            self.connection.commit()

            return item
        except Exception as e:
            from scrapy.exceptions import DropItem

            self.connection.rollback()
            raise DropItem(f"DBItemPipeline error: {e}, item: {item}") from e

    @override
    def close_spider(self, spider) -> None:
        """
        Close the spider and close the database connection.
        """
        self.cursor.close()
        self.connection.close()
