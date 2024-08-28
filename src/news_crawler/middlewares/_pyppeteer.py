# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


from collections.abc import Awaitable
from typing import Callable, Optional

from pyppeteer.browser import Browser
from pyppeteer.page import Page
from scrapy import Spider, signals
from scrapy.crawler import Crawler

from ..requests._pyppeteer import PyppeteerRequest
from ..response._pyppeteer import PyppeteerResponse

__all__ = ["PyppeteerDownloaderMiddleware"]


class PyppeteerDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    async def _get_page(self) -> Page:
        page = await self.browser.newPage()

        return page

    # async def

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    async def process_request(self, request: PyppeteerRequest, spider: Spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        if request.meta.get("pyppeteer", False) and isinstance(
            request, PyppeteerRequest
        ):
            spider.logger.info(f"pyppeteer request: {request.url}")
            page = await self._get_page()
            response = await page.goto(request.url)

            pyppeteer_callback: Optional[Callable[[Page], Awaitable[None]]] = (
                request.meta.get("pyppeteer_process_request_callback", None)
            )

            if pyppeteer_callback:
                await pyppeteer_callback(page)

            content = await page.content()

            return PyppeteerResponse(
                url=request.url,
                body=bytes(content, encoding="utf-8"),
                headers=response.headers or request.headers,  # type: ignore
                request=request,
                status=response.status,  # type: ignore
                cookies=await page.cookies(),
            )

        return None

    async def spider_opened(self, spider: Spider):
        from pyppeteer import launch

        width, height = 1366, 768

        spider.logger.info(f"async Spider opened: {spider.name}")

        self.browser: Browser = await launch(
            executablePath="/Users/jiangjunlong/code/python/news-crawler/other/chrome-mac/Chromium.app/Contents/MacOS/Chromium",
            headless=False,
            userDataDir="./other/userdata",
            args=["--disable-infobars", f"--window-size={width},{height}"],
        )
