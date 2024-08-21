from typing import Optional

from scrapy import Request, Spider
from typing_extensions import override

from .base import BaseMiddleware

__all__ = ["CategoryFilterMiddleware"]


class CategoryFilterMiddleware(BaseMiddleware):
    def _get_category_id(self, url: str) -> Optional[str]:
        from re import findall

        try:
            return findall(r"/story/(\d+)/", url)[0]
        except IndexError:
            return None

    @override
    def process_request(self, request: Request, spider: Spider) -> None:
        url: str = request.url
        category_id = self._get_category_id(url)

        if (self.allowed_categories is None) or (category_id is None):
            return None

        if category_id in self.allowed_categories:
            return None

        from scrapy.exceptions import IgnoreRequest

        spider.logger.info(
            f"Ignoring request for URL: {url} with category_id: {category_id}"
        )

        raise IgnoreRequest(f"Category ID {category_id} is not allowed for URL: {url}")

    @override
    def spider_opened(self, spider: Spider) -> None:
        self.allowed_categories: Optional[list[int]] = getattr(
            spider, "allowed_categories", None
        )

        return super().spider_opened(spider)
