from scrapy import Field, Item


class CnyesNewsItem(Item):
    news_url = Field()  # BASE_URL/data.newsId
    title = Field()  # data.title
    content = Field()  # data.content
    date = Field()  # timestamp_to_datetime(data.publishAt) -> date_string
