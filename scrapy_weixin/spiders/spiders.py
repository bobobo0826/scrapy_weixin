#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import time
import os
from selenium import webdriver
import re
import json
import bs4
import requests
from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider,Rule
from scrapy.http import Request
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy_weixin.items import ScrapyWeixinItem
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class ShareditorSpider(scrapy.Spider):
    name = "scrapy_weixin"
    allowed_domains = ["weixin.sogou.com"]
    accountList = ["小年夜"]
    title_index = 1

    # accountList = ['苹果', "养生", "电器", "星座", "新闻", "八卦", "C", "电脑", "手机"]
    path = os.path.join(os.getcwd(), time.strftime('%Y-%m-%d_%H-%M-%S'))
    try:
        os.makedirs(path)
    except OSError:
        print("folder not exist!")

    def __init__(self):

        time.sleep(5)
        # 初始化时候，给爬虫新开一个浏览器
        self.browser = webdriver.Chrome()
        self.browser.maximize_window()
        super(scrapy.Spider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)



    def start_requests(self):

        for index, account in enumerate(self.accountList):
            print("index=", index, "account", account)
            url = "http://weixin.sogou.com/weixin?type=1&s_from=input&query="+account# 获取公众号链接
            request = Request(url=url, callback=self.parse, dont_filter=True)
            request.meta['PhantomJS'] = True
            yield request


    def parse(self, response):
        selector = Selector(response)
        account = selector.xpath('//li/div/div[2]/p[1]/a/@href').extract()
        for i, acc in enumerate(account):
            print("i=", i, "acc=", acc)
            request = Request(url=acc, callback=self.parse_profile, dont_filter=True)
            request.meta['PhantomJS'] = True
            yield request

        # 测试爬第一条
        # request = Request(url=account[0], callback=self.parse_profile, dont_filter=True)
        # request.meta['PhantomJS'] = True
        # yield request

        url_next = selector.xpath('//*[@id="sogou_next"]/@href').extract_first()
        if url_next:
            str_url = url_next.split("&s_from=input")
            url_pro = "http://weixin.sogou.com/weixin" + str_url[0] + "&_sug_type_=&s_from=input&_sug_=n" + str_url[1]
            yield Request(url=url_pro,  callback=self.parse, dont_filter=True)

    def parse_profile(self, response):
        selector = Selector(response)
        article = selector.xpath('//h4[@class="weui_media_title"]/@hrefs').extract()
        for i in range(len(article)):
            articleURL = "https://mp.weixin.qq.com"+article[i]
            request = Request(url=articleURL, callback=self.parse_basic, dont_filter=True)
            request.meta['PhantomJS'] = True
            yield request

        #测试爬第一条
        # articleURL = "https://mp.weixin.qq.com" + article[0]
        # request = Request(url=articleURL, callback=self.parse_basic, dont_filter=True)
        # request.meta['PhantomJS'] = True
        # yield request

    def parse_basic(self, response):
        selector = Selector(response)
        item = ScrapyWeixinItem()
        article_url = response.request.url
        original_title = selector.xpath('//*[@id="activity-name"]/text()').extract_first().replace(" ", "").replace("\n", "")
        article_date =selector.xpath('//*[@id="post-date"]/text()').extract_first()
        scrapy_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        sub_public = selector.xpath('//*[@id="post-user"]/text()').extract_first()
        picture = selector.xpath('//img/@data-src').extract()
        self.title_index = self.title_index +1
        if "|" in original_title:
            title = original_title.replace("|", "")
        else:
            title = original_title
        page = requests.get(article_url)
        page.encoding = 'utf-8'
        soup = BeautifulSoup(str(page.text), 'html.parser')
        article = soup.select('.rich_media_content')[0].text
        myfile = open("{}\{}.html".format(self.path.replace("\\\\", "\\"), (str(self.title_index)+title)), 'wb')
        myfile.write(response.body)
        myfile.close()
        item["article_url"] = article_url
        item["title"] = title
        item["article"] = article
        if picture:
            item["picture"] = picture
        item["sub_public"] = sub_public
        item["article_date"] = article_date
        item["scrapy_date"] = scrapy_date
        item["html"] = response.body.decode('utf-8')
        yield item

    def spider_closed(self, spider):
        # 当爬虫退出的时候关闭chrome
        print("spider closed")
        time.sleep(60)
        self.browser.quit()


