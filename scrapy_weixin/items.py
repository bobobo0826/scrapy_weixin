# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyWeixinItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    sub_public = scrapy.Field()
    title = scrapy.Field()
    article_url = scrapy.Field()
    article_date = scrapy.Field()
    scrapy_date = scrapy.Field()
    article = scrapy.Field()
    picture = scrapy.Field()
    html = scrapy.Field()
    pass
