from typing import Optional

from scrapy import Request, Spider, signals
from scrapy.crawler import Crawler
from typing_extensions import Self

# from .base import BaseMiddleware

__all__ = ["CategoryFilterMiddleware"]

category_filter_map = {
    "udn": "story",
    "money_udn": "story",
    "cna": "news",
}


class CategoryFilterMiddleware:
    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        instance = cls()

        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)

        return instance

    def _get_category_id(self, url: str, spider_name: str) -> Optional[str]:
        from re import findall

        try:
            return findall(rf"/{category_filter_map[spider_name]}/(\d+)/", url)[0]
        except (IndexError, KeyError):
            return None

    def process_request(self, request: Request, spider: Spider) -> None:
        url: str = request.url
        category_id = self._get_category_id(url, spider.name)

        if (self.allowed_categories is None) or (category_id is None):
            return None

        if category_id in self.allowed_categories:
            return None

        from scrapy.exceptions import IgnoreRequest

        spider.logger.info(
            f"Ignoring request for URL: {url} with category_id: {category_id}"
        )

        raise IgnoreRequest(f"Category ID {category_id} is not allowed for URL: {url}")

    def spider_opened(self, spider: Spider) -> None:
        self.allowed_categories: Optional[set[int]] = getattr(
            spider, "allowed_categories", None
        )

        return None
