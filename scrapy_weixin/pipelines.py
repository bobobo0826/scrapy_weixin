# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy_weixin.items import ScrapyWeixinItem

class ScrapyWeixinPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["weixin"]
        self.Article = db["text"]

    def process_item(self, item, spider):
        if isinstance(item, ScrapyWeixinItem):
            try:
                # self.Article.insert(dict(item))
                self.Article.insert(dict(item))
            except Exception:
                pass
        return item