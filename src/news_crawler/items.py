# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


from scrapy import Field, Item


class NewsItem(Item):
    news_url = Field()  # BASE_URL/data.newsId
    title = Field()  # data.title
    content = Field()  # data.content
    created_at = Field()  # timestamp_to_datetime(data.publishAt) -> date_string
