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
    allowed_categories: set[int] = {
        # 產業
        5612,  # 產業熱點
        11162,  # 科技產業
        10871,  # 綜合產業
        124092,  # AI IP大進擊
        6808,  # 產業達人
        # 要聞
        7307,  # 政經焦點
        12926,  # 今晨必讀,
        123742,  # 深度報導
        10869,  # 總經趨勢
        122335,  # 經濟周報
        8888,  # 大數字
        # 證券
        5607,  # 市場焦點
        5710,  # 集中市場
        11074,  # 櫃買動態
        123397,  # 台股擂台
        12509,  # AI 人機協作
    }

    name = "money_udn"
    allowed_domains = ["money.udn.com"]
    start_urls = [f"{news_list_base_url}/{page}?_={get_timestamp_ms()}"]

    def _make_next_url(self):
        self.page = self.page + 1

        return f"{self.news_list_base_url}/{self.page}?_={get_timestamp_ms()}"

    @override
    def parse(self, response: HtmlResponse) -> Generator[Request, None, None]:
        yield from self._parse_news_list(response)

        yield Request(url=self._make_next_url(), callback=self.parse)

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
        item["created_at"] = self.get_datetime(
            response.css("time.article-body__time::text").get().__str__()
        )

        yield item
