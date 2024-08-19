from collections.abc import Generator
from datetime import datetime

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.spiders import Spider
from typing_extensions import override

from ..items import NewsItem

__all__ = ["MoneyUdnSpider"]


def get_timestamp_ms() -> int:
    return int(datetime.now().timestamp() * 1000)


class MoneyUdnSpider(Spider):
    date_format = "%Y/%m/%d %H:%M:%S"  # 2024/08/18 22:30:49

    news_list_base_url = "https://money.udn.com/rank/ajax_newest/1001/0"
    refer_path = "?from=edn_newestlist_rank"
    page = 1

    name = "money_udn"
    allowed_domains = ["money.udn.com"]
    start_urls = [f"{news_list_base_url}/{page}?_={get_timestamp_ms()}"]

    def _make_next_url(self):
        return f"{self.news_list_base_url}/{self.page + 1}?_={get_timestamp_ms()}"

    @override
    def parse(self, response: HtmlResponse) -> Generator[Request, None, None]:
        yield from self._parse_news_list(response)

    def get_datetime(self, date_string: str) -> datetime:
        from ..utils._datetime import date_string_to_datetime

        return date_string_to_datetime(date_string=date_string, format=self.date_format)

    def _parse_news_list(
        self, response: HtmlResponse
    ) -> Generator[Request, None, None]:
        from urllib.parse import urljoin

        hrefs = response.css("a::attr(href)").getall()

        for href in hrefs:
            yield Request(url=urljoin(href, self.refer_path), callback=self._parse_news)

    def _parse_news(self, response: HtmlResponse) -> Generator[NewsItem, None, None]:
        item = NewsItem()

        content = "".join(response.css("#article_body p::text").getall())

        item["news_url"] = response.url
        item["content"] = content
        item["title"] = response.css("#story_art_title::text").get().__str__()
        item["date"] = self.get_datetime(
            response.css("time.article-body__time::text").get().__str__()
        )

        yield item
