from datetime import datetime
from typing import Optional

from scrapy import Item
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem
from scrapy.spiders import Spider
from typing_extensions import override

from ..config import PROJECT_BASE_PATH
from ..processer.states import CrawlStateProcesser
from .base import BasePipeline

__all__ = ["TimeBoundaryPipeline"]


class TimeBoundaryPipeline(BasePipeline):
    @override
    def __init__(self, crawler: Crawler):
        self.crawler = crawler

        self.last_start_time: Optional[datetime] = None

        self._is_sucess = False
        self.start_time = datetime.now()

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """
        工廠方法，用於創建 pipeline 實例並傳遞 crawler 對象。

        Args:
            crawler (Crawler): Scrapy 的 Crawler 實例。

        Returns:
            BasePipeline: 初始化後的 BasePipeline 實例。
        """
        return cls(crawler)

    @override
    def open_spider(self, spider: Spider):
        self.state_processer = CrawlStateProcesser(
            base_filepath=PROJECT_BASE_PATH,
            name=spider.name,  # type: ignore
        )

        self.last_start_time = self.state_processer.state["last_start_time"]  # type: ignore

    @override
    def process_item(self, item: Item, spider) -> Item:
        """
        處理每一個從爬蟲中傳遞過來的 item。如果 item 的時間早於上次啟動時間，則關閉爬蟲。
        :param item: 從爬蟲傳遞過來的 item
        :param spider: 當前處理 item 的爬蟲對象
        :return: 返回處理後的 item 或者 raise DropItem 異常
        """
        from ..utils._datetime import datetime_to_date_string

        publish_at: datetime = item["date"]

        if publish_at < self.last_start_time:  # type: ignore
            # 如果 item 的時間早於上次啟動時間，關閉爬蟲
            self._is_sucess = True
            self.crawler.engine.close_spider(  # type: ignore
                spider=spider, reason="Reached the last start time threshold"
            )

            raise DropItem("Reached the last start time threshold")

        item_key = self.state_processer.generate_item_key(
            title=item["title"], date=item["date"]
        )

        if self.state_processer.is_item_processed(item_key=item_key):
            raise DropItem(f"Duplicate item found: {item['title']}")

        item["date"] = datetime_to_date_string(publish_at, format="%Y%m%d %H%M")
        self.state_processer.mark_item_processed(item_key=item_key)

        return item

    @override
    def close_spider(self, spider):
        self.state_processer.write_state(
            is_success=self._is_sucess,
            success_or_error_time=self.start_time
            if self._is_sucess
            else self.last_start_time,  # type: ignore
        )
