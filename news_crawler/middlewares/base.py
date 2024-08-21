from scrapy import Request, Spider, signals
from scrapy.crawler import Crawler
from typing_extensions import Self

__all__ = ["BaseMiddleware"]


class BaseMiddleware:
    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        instance = cls()

        crawler.signals.connect(instance.spider_opened, signal=signals.spider_opened)

        return instance

    def process_request(self, request: Request, spider: Spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def spider_opened(self, spider: Spider) -> None: ...
