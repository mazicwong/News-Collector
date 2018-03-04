#!/usr/bin/env python
# coding=utf-8
import json

import requests
import scrapy
import re

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from crawl.items import SinaItem
from scrapy.http import Request
from urllib.request import urlopen
from crawl.jsphlim.tool import ListCombiner


class SinaNewsSpider(scrapy.Spider):
    name = 'sina_news_spider'  #最后要调用的名字
    start_urls = ['http://news.sina.com.cn'] #起始地址
    allowed_domains = ['sina.com.cn']  #过滤器

    url_pattern = r'http://(\w+)\.sina.com.cn/(\w+)/(\d{4}-\d{2}-\d{2})/doc-([a-zA-Z0-9]{15}).(?:s)html' #匹配新浪新闻的正则表达式
    pattern = "<meta name=\"sudameta\" content=\"comment_channel:(\w+);comment_id:comos-([a-zA-Z0-9]{14})\" />"  #匹配评论channel的正则表达式
    # http://comment5.news.sina.com.cn/comment/skin/default.html?channel=gj&newsid=comos-fyrkuxt0757134&group=0
    def parse(self, response):  # response即网页数据
        pat = re.compile(self.url_pattern)
        next_urls = re.findall(pat, str(response.body))
        for url in next_urls:
            article = 'http://'+url[0]+'.sina.com.cn/'+url[1]+'/'+url[2]+'/doc-'+url[3]+'.shtml' #拼凑出新闻链接
            print(article)
            yield Request(article,callback=self.parse_news)

    def parse_news(self, response):
        item = SinaItem()
        pattern = re.match(self.url_pattern, str(response.url))
        item['source'] = 'sina'
        item['date'] = ListCombiner(str(pattern.group(3)).split('-'))
        print(item['date'])

        sel = requests.get(response.url)
        sel.encoding = 'utf-8'
        sel = sel.text
        pat = re.compile(self.pattern)
        res = re.findall(pat, str(sel))  #获取该新闻评论的channel信息 以便构造出链接
        if res == []: return
        commentsUrl = 'http://comment5.news.sina.com.cn/comment/skin/default.html?channel='+str(res[0][0])+'&newsid=comos-'+str(res[0][1])+'&group=0' #新闻评论链接
        soup = BeautifulSoup(sel,'html.parser')
        title = soup.find('h1',class_='main-title')  #坑点啊 新浪新闻不同类型的新闻html不太一样 所以需要两种情况来处理
        if title == None:
            title = soup.find('h1',id='main_title')

        title = title.text #获取标题内容

        temp = BeautifulSoup(str(soup.find('div',id='article')),'html.parser')  #两种不同情况的处理
        temp1 = BeautifulSoup(str(soup.find('div',id='artibody')),'html.parser')
        if len(temp.text)>len(temp1.text):
            temps = temp.find_all('p')
        else:
            temps = temp1.find_all('p')

        passage = ''  #拼凑新闻内容
        for new in temps:
            passage+=new.text

        item['newsId'] = 'comos-'+str(res[0][1])
        item['cmtId'] = item['newsId']
        item['channelId'] = str(res[0][0])
        item['comments'] = {'link': str(commentsUrl)}
        item['contents'] = {'link': str(response.url), 'title': u'', 'passage': u''}
        item['contents']['title'] = title
        item['contents']['passage'] = passage
        yield item




