#!/usr/bin/env python
# coding=utf-8

from scrapy import cmdline
#cmdline.execute("scrapy crawl netease_news_spider".split())
#cmdline.execute("scrapy crawl tencent_news_spider".split())
cmdline.execute("scrapy crawl sina_news_spider".split())
