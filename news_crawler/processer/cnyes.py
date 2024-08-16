from collections.abc import Generator
from datetime import datetime
from typing import Any

from typing_extensions import override

from ..items import NewsItem
from ..types.crawler_state import CrawlerState
from ..utils._html import get_text
from .base import WebSiteNewsBaseProcesser


class CnyesWebSiteNewsProcesser(WebSiteNewsBaseProcesser):
    base_url = "https://news.cnyes.com/news/id"

    @override
    @classmethod
    def process(
        cls,
        all_news: list[dict[str, Any]],
        last_start_time: datetime = datetime(
            year=2024, month=7, day=31, hour=0, minute=0, second=0
        ),
    ) -> Generator[NewsItem, None, CrawlerState]:
        from ..utils._datetime import datetime_to_date_string, timestamp_to_datetime

        processing_complete: bool = True
        scraped_items_count: int = 0

        for news in all_news:
            if (
                publishAt := timestamp_to_datetime(news["publishAt"])
            ) >= last_start_time:
                item = NewsItem()

                item["news_url"] = f'{cls.base_url}/{news["newsId"]}'
                item["title"] = news["title"]
                item["content"] = get_text(html_string=news["content"], element="p")
                item["date"] = datetime_to_date_string(publishAt, format="%Y%m%d %H%M")

                scraped_items_count += 1
                yield item
            else:
                processing_complete = False
                break

        return CrawlerState(
            name="cnyes",
            scraped_items_count=scraped_items_count,
            processing_complete=processing_complete,
        )
