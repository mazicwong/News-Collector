# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item,Field

class NewsItem(Item):
    source = Field()
    date = Field()
    newsId = Field()
    cmtId = Field()
    contents = Field()
    comments = Field()

class CrawlItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NeteaseItem(NewsItem):
    boardId = Field()

class TencentItem(NewsItem):
    pass

class SinaItem(NewsItem):
    channelId = Field()
