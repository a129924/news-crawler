from typing_extensions import TypedDict


class CrawlerState(TypedDict):
    name: str
    scraped_items_count: int
    processing_complete: bool
