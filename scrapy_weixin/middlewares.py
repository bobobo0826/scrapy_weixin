# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import base64
import time
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy_weixin.ipList import getProxy
#scrapy crawl scrapy_weixin
class PhantomJSMiddleware(object):
    def process_request(self, request, spider):
        if 'PhantomJS'in request.meta:
            #设置代理ip
            ip = getProxy()
            proxy = Proxy(
                {
                    'proxyType': ProxyType.MANUAL,
                    'httpProxy': ip  # 代理ip和端口
                }
            )
            if "https://mp.weixin.qq.comhttp//" in request.url:
                a = request.url.replace("https://mp.weixin.qq.comhttp//", "https://")
                if "#wechat_redirect" in a:
                    b = a.replace("#wechat_redirect", "")
                    true_url = b
                else:
                    true_url = a
            else:
                true_url = request.url
            desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
            # 把代理ip加入到技能中
            proxy.add_to_capabilities(desired_capabilities)
            driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
            driver.get(true_url)
            time.sleep(5)  # 等待JS执行
            content = driver.page_source
            while "验证码" or "<html><head></head><body></body></html>" or "Please check your username and password" in content:
                print("需等待重新获取ip。。。")
                time.sleep(5)
                new_ip = getProxy()
                print("new_ip=================", new_ip)
                while new_ip == ip:
                    time.sleep(5)
                    new_ip = getProxy()
                    print("new_ip=================",new_ip)
                proxy = Proxy(
                    {
                        'proxyType': ProxyType.MANUAL,
                        'httpProxy': new_ip  # 代理ip和端口
                    }
                )
                desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
                proxy.add_to_capabilities(desired_capabilities)
                driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
                driver.get(true_url)
                time.sleep(5)  # 等待JS执行
                content = driver.page_source
            driver.quit()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)

class JavaScriptMiddleware(object):
    def process_request(self, request, spider):
        if "https://mp.weixin.qq.comhttp//" in request.url:
            a = request.url.replace("https://mp.weixin.qq.comhttp//", "https://")
            if "#wechat_redirect" in a:
                b = a.replace("#wechat_redirect", "")
                true_url= b
            else:
                true_url=a
        else:
            true_url = request.url
        spider.browser.get(true_url)
        time.sleep(10)  # 等待JS执行
        content = spider.browser.page_source
        while "验证码" in content:
            print("需输入验证码。。。")
            time.sleep(60)
            spider.browser.get(true_url)
            time.sleep(10)  # 等待JS执行
            content = spider.browser.page_source
        return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)