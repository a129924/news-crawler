from collections.abc import Generator
from typing import Any, Optional, Union
from urllib.parse import urljoin

from scrapy import Item, Request, Spider
from scrapy.http import HtmlResponse
from typing_extensions import override

from ..config.headers import CnyesHeaders

__all__ = ["CnyesSpider"]


class CnyesSpider(Spider):
    name = "cnyes"
    allowed_domains = ["api.cnyes.com"]
    start_urls = [
        "https://api.cnyes.com/media/api/v1/newslist/category/headline?limit=30&page=1"
    ]
    custom_settings: dict[str, Any] = {"DEFAULT_REQUEST_HEADERS": CnyesHeaders}
    base_url = "https://news.cnyes.com/news/id"

    @override
    def parse(
        self, response: HtmlResponse
    ) -> Generator[Union[Item, Request], None, None]:
        from ..items import CnyesNewsItem
        from ..utils._datetime import timestamp_to_datetime
        from ..utils._html import get_text

        items: dict[str, Any] = response.json()["items"]  # type: ignore

        for news in items["data"]:
            item = CnyesNewsItem()

            item["news_url"] = f'{self.base_url}/{news["newsId"]}'
            item["title"] = news["title"]
            item["content"] = get_text(html_string=news["content"], element="p")
            item["date"] = timestamp_to_datetime(news["publishAt"])

            yield item

        # try:
        #     while True:
        #         yield next(news_generator)

        # except StopIteration as error:
        #     state = error.value
        #     next_page_url: Optional[str] = items.get("next_page_url", None)

        #     if state["processing_complete"]:
        #         self.logger.info("成功")

        #         if next_page_url:
        #             yield Request(
        #                 url=urljoin(response.url, next_page_url), callback=self.parse
        #             )

        #     else:
        #         # raise StopIteration(
        #         #     f"已超過上一次的運行時間 '{datetime_to_date_string(last_start_time, '%Y%m%d %H%M')}'"
        #         # )
        #         self.logger.info(msg="已超過上一次的運行時間")
