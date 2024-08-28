from collections.abc import Generator, Iterable
from typing import Any

from scrapy import Spider
from scrapy.exceptions import CloseSpider
from scrapy.http import HtmlResponse, Request
from typing_extensions import override

from ..config.headers import CnaHeader
from ..items import NewsItem

__all__ = ["CnaSpider"]


class CnaSpider(Spider):
    date_format = "%Y/%m/%d %H:%M"  # 2024/08/22 10:30
    name = "cna"
    page = 7
    allowed_domains = ["cna.com.tw"]
    start_urls = ["https://www.cna.com.tw/cna2018api/api/WNewsList"]
    custom_settings = {"DEFAULT_REQUEST_HEADERS": CnaHeader}

    referer = {"Referer": "https://www.cna.com.tw/list/acul.aspx"}

    @property
    def body(self):
        from json import dumps

        self.page += 1

        return dumps(
            {
                "action": "0",
                "category": "aall",
                "pagesize": "20",
                "pageidx": self.page,
            }
        )

    def _process_news_content(self, response: HtmlResponse) -> str:
        return "".join(response.css(".paragraph p::text").getall())

    @override
    def start_requests(self) -> Iterable[Request]:
        for url in self.start_urls:
            yield Request(
                url=url,
                method="POST",
                body=self.body,
                callback=self._parse_news_list,
            )

    def _parse_news_list(
        self, response: HtmlResponse
    ) -> Generator[Request, None, None]:
        news_items: list[dict[str, Any]] = response.json()["ResultData"]["Items"]  # type: ignore

        if len(news_items) == 0:
            raise CloseSpider("No more items to process")

        for news_item in news_items:
            yield response.follow(
                url=news_item["PageUrl"],
                method="GET",
                meta={
                    "title": news_item["HeadLine"],
                    "date": news_item["CreateTime"],
                },
                callback=self._parse_news,
                headers=self.referer,
            )

        yield response.follow(
            url=self.start_urls[0],
            method="POST",
            body=self.body,
            callback=self._parse_news_list,
        )

    def _parse_news(self, response: HtmlResponse) -> Generator[NewsItem, None, None]:
        from datetime import datetime

        item = NewsItem()

        item["news_url"] = response.url
        item["title"] = response.meta["title"]
        item["content"] = self._process_news_content(response=response)
        item["date"] = datetime.strptime(response.meta["date"], self.date_format)

        yield item
