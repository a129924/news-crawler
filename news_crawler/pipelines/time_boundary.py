from datetime import datetime
from typing import Optional

from scrapy.exceptions import CloseSpider
from scrapy.spiders import Spider
from typing_extensions import override

from ..config import PROJECT_BASE_PATH
from ..processer.states import CrawlStateProcesser
from .base import BasePipeline

__all__ = ["TimeBoundaryPipeline"]


class TimeBoundaryPipeline(BasePipeline):
    # FIXME: 要修改因為意外錯誤連跳出紀錄爬取到的新聞日期
    def __init__(self):
        self.last_start_time: Optional[datetime] = None

        self._is_sucess = True
        self.last_error_date: Optional[datetime] = None

    @override
    def open_spider(self, spider: Spider):
        print("open_spdier", "spider.name", spider.name)

        self.state_processer = CrawlStateProcesser(
            base_filepath=PROJECT_BASE_PATH,
            name=spider.name,  # type: ignore
        )

        self.last_start_time = self.state_processer.state["last_start_time"]

    @override
    def process_item(self, item, spider):
        """
        處理每一個從爬蟲中傳遞過來的 item。如果 item 的時間早於上次啟動時間，則關閉爬蟲。
        :param item: 從爬蟲傳遞過來的 item
        :param spider: 當前處理 item 的爬蟲對象
        :return: 返回處理後的 item 或者 raise CloseSpider 異常
        """
        from ..utils._datetime import datetime_to_date_string

        publish_at: datetime = item["date"]

        try:
            if publish_at < self.last_start_time:  # type: ignore
                # 如果 item 的時間早於上次啟動時間，關閉爬蟲

                raise CloseSpider("Reached the last start time threshold")

            item["date"] = datetime_to_date_string(publish_at, format="%Y%m%d %H%M")

            return item

        except Exception:
            self._is_sucess = False
            self.last_error_date = publish_at

    @override
    def close_spider(self, spider):
        self.state_processer.write_state(self.last_error_date)
