# scrapy_weixin：scrapy框架中爬取微信公众号

1、由于代理ip可能失效，为避免程序无法运行，将代理ip的中间件注释了
    如需要设置代理ip，要在settings.py中取消PlantomJSMiddleware注释，同时将JavaScriptMiddleware注释
    
2、可指定公众号或关键字

3、运行时在终端输入：scrapy crawl scrapy_weixin

4、爬取的数据保存在MongoDB weixin text 中，同时爬取的公众号文章以html文件的形式保存在当前文件夹下，文件夹以当前爬取时间命名
