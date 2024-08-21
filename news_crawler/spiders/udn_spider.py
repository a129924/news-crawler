from collections.abc import Generator
from typing import Literal

from scrapy import Request
from scrapy.http import HtmlResponse
from scrapy.spiders import Spider
from typing_extensions import override

from ..items import NewsItem


def api_base_url(page: int) -> str:
    return f"https://udn.com/api/more?page={page}&id=&channelId=1"


class UdnSpider(Spider):
    date_format = "%Y-%m-%d %H:%M"  # "2024-08-21 10:29"
    page = 0

    name = "udn"
    allowed_domains = ["udn.com"]
    start_urls = ["https://udn.com/news/breaknews/1"]

    base_url = "https://udn.com"
    data_query_map: dict[Literal["data_query"], str] = {}

    def _get_data_query(self, response: HtmlResponse):
        def mix_key_value(json_string: str) -> str:
            from json import loads
            from urllib.parse import urlencode

            """
            '{&quot;cate_id&quot;:&quot;0&quot;,&quot;type&quot;:&quot;breaknews&quot;,&quot;totalRecNo&quot;:&quot;34325&quot;,&quot;page&quot;:7}'
            "{'cate_id': '0','type':'breaknews','totalRecNo':'34334'}"
            cate_id=0&type=breaknews&totalRecNo=34325
            """
            return urlencode(loads(json_string.replace("'", '"')))

        return mix_key_value(
            response.css("#indicator::attr(data-query)").get()  # type: ignore
        )

    def _set_data_query(self, response: HtmlResponse) -> None:
        if "data_query" not in self.data_query_map:
            self.data_query_map["data_query"] = self._get_data_query(response=response)

    def _make_next_api_url(self):
        self.page += 1

        return f"{api_base_url(page=self.page)}&{self.data_query_map['data_query']}"

    def _schedule_next_page(self) -> Request:
        next_page_url = self._make_next_api_url()

        return Request(url=next_page_url, callback=self._parse_news_list)

    def _process_news_content(self, response: HtmlResponse) -> str:
        return "".join(
            response.css(".article-content__editor p::text").getall()
        ).replace("\r\n", "")

    @override
    def parse(self, response: HtmlResponse) -> Generator[Request, None, None]:
        self._set_data_query(response=response)

        yield self._schedule_next_page()

    def _parse_news_list(
        self, response: HtmlResponse
    ) -> Generator[Request, None, None]:
        for news_item in response.json()["lists"]:  # type: ignore
            """
            "/news/story/7266/8173730?from=udn-ch1_breaknews-1-0-news"
            """
            yield Request(
                f"{self.base_url}{news_item['titleLink']}",
                callback=self._parse_news,
                meta={
                    "title": news_item["title"],
                    "date": news_item["time"]["date"],  # "2024-08-21 10:29"
                },
            )

        yield self._schedule_next_page()

    def _parse_news(self, response: HtmlResponse) -> Generator[NewsItem, None, None]:
        from datetime import datetime

        item = NewsItem()

        item["news_url"] = response.url
        item["title"] = response.meta["title"]
        item["content"] = self._process_news_content(response=response)
        item["date"] = datetime.strptime(response.meta["date"], self.date_format)

        yield item
