# -*- coding: utf-8 -*-
from scrapy.http import HtmlResponse
import time
import random
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scrapy_weixin.ipList import PROXIES
ip = PROXIES
print("ip=======", ip)
proxy = Proxy(
{
'proxyType': ProxyType.MANUAL,
'httpProxy': ip  # 代理ip和端口
}
)
# 新建一个“期望技能”，哈哈
desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# 把代理ip加入到技能中
proxy.add_to_capabilities(desired_capabilities)
driver = webdriver.PhantomJS(desired_capabilities=desired_capabilities)
driver = webdriver.PhantomJS()
# print(request.url)
driver.get("http://weixin.sogou.com/weixin?type=1&s_from=input&query=h")
time.sleep(3)  # 等待JS执行
content = driver.page_source
print("content---------------------")
print(content)
driver.quit()