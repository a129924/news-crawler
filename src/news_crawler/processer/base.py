from collections.abc import Generator
from typing import Any

from scrapy import Item

from ..types.crawler_state import CrawlerState


class WebSiteNewsBaseProcesser:
    base_url: str

    def process(
        self, all_news: list[Any], **kwargs: Any
    ) -> Generator[Item, Any, CrawlerState]:
        raise NotImplementedError("該function必須override")
