from scrapy import Spider
from scrapy.exporters import CsvItemExporter
from typing_extensions import override

from .base import BasePipeline

__all__ = ["CsvItemPipeline"]


class CsvItemPipeline(BasePipeline):
    def __init__(self) -> None:
        self.file = open("output.csv", "wb")
        self.exporter = CsvItemExporter(self.file, encoding="UTF-8")
        self.exporter.start_exporting()

    @override
    def process_item(self, item, spider):
        self.exporter.export_item(item)

        return item

    @override
    def close_spider(self, spider: Spider):
        self.exporter.finish_exporting()
        self.file.close()
