from scrapy import Spider
from scrapy.crawler import Crawler
from scrapy.exporters import CsvItemExporter
from typing_extensions import override

from .base import BasePipeline

__all__ = ["CsvItemPipeline"]


class CsvItemPipeline(BasePipeline):
    def __init__(self, spider_name: str) -> None:
        self.file = open(f"{spider_name}_output.csv", "wb")
        self.exporter = CsvItemExporter(self.file, encoding="UTF-8")
        self.exporter.start_exporting()

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        spider_name = crawler.spider.name  # type: ignore # 獲取爬蟲名稱

        return cls(spider_name)

    @override
    def process_item(self, item, spider):
        self.exporter.export_item(item)

        return item

    @override
    def close_spider(self, spider: Spider):
        self.exporter.finish_exporting()
        self.file.close()
