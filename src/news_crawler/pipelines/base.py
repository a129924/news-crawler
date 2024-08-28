class BasePipeline:
    def open_spider(self, spider):
        """
        當爬蟲啟動時調用。可以在這裡執行一些初始化操作。
        :param spider: 當前啟動的爬蟲對象
        """

    def close_spider(self, spider):
        """
        當爬蟲關閉時調用。可以在這裡執行一些清理操作。
        :param spider: 當前關閉的爬蟲對象
        """

    def process_item(self, item, spider):
        """
        處理每一個從爬蟲中傳遞過來的 item。必須返回一個 dict、Item 對象或者 raise DropItem。
        :param item: 從爬蟲傳遞過來的 item
        :param spider: 當前處理 item 的爬蟲對象
        :return: 返回處理後的 item
        """
        return item
