#!/usr/bin/env python
# coding=utf-8
import json

import requests
import scrapy
import re

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from crawl.items import SinaItem,NeteaseItem,TencentItem
from scrapy.http import Request
from urllib.request import urlopen
from crawl.maziclib.news_fun import ListCombiner


class NeteaseNewsSpider(scrapy.Spider):
    name = 'netease_news_spider'  # 最后要调用的名字
    start_urls = ['https://news.163.com']
    allowed_domains = ['news.163.com']

    url_pattern = r'(https://news\.163\.com)/(\d{2})/(\d{4})/(\d+)/(\w+)\.html'

    def parse(self, response):  # response即网页数据
        pat = re.compile(self.url_pattern)
        next_urls = re.findall(pat, str(response.body))

        ###debug
        # article = next_urls[0][0]+'/'+next_urls[0][1]+'/'+next_urls[0][2]+'/'+next_urls[0][3]+'/'+next_urls[0][4]+'.html'
        # yield Request(article, callback=self.parse_news)
        ###debug

        for next_url in next_urls:
            article = next_url[0] + '/' + next_url[1] + '/' + next_url[2] + '/' + next_url[3] + '/' + next_url[4] + '.html'
            yield Request(article, callback=self.parse_news)

    def parse_news(self, response):
        item = NeteaseItem()
        selector = Selector(response)
        pattern = re.match(self.url_pattern, response.url)

        source = 'netease'
        date = '20' + pattern.group(2) + pattern.group(3)
        newsId = pattern.group(5)
        cmtId = pattern.group(5)

        productKey = re.findall(re.compile(r'"productKey" : "(\w+)"'), str(response.body))[0]
        comments_api = 'https://comment.news.163.com/api/v1/products/' + productKey + '/threads/' + newsId
        boardId = re.findall(r'"boardId":"(\w+)"', str(urlopen(comments_api).read()))[0]
        comments = ('https://comment.news.163.com/' + boardId + '/' + newsId + '.html')

        item['source'] = 'netease'
        item['date'] = date
        item['newsId'] = newsId
        item['cmtId'] = cmtId
        # item['boardId'] = boardId
        item['comments'] = {'link': comments}
        item['contents'] = {'link': str(response.url), 'title': u'', 'passage': u''}
        item['contents']['title'] = selector.xpath('//*[@id="epContentLeft"]/h1/text()').extract()[0]
        item['contents']['passage'] = ListCombiner(selector.xpath('//*[@id="endText"]/p/text()').extract())
        yield item

class TencentNewsSpider(scrapy.Spider):
    name = 'tencent_news_spider'  # 最后要调用的名字
    start_urls = ['http://www.qq.com']
    allowed_domains = ['new.qq.com']

    # https://new.qq.com/omn/20180903/20180903A1Z1BM.html
    url_pattern = r'http://new\.qq\.com/(\w+)/(\d{8})/(\w+)\.html'

    def parse(self, response):  # response即网页数据
        # print(response.text)
        pat = re.compile(self.url_pattern)
        next_urls = re.findall(pat, str(response.body))

        for next_url in next_urls:
            article = 'http://new.qq.com/'+next_url[0]+'/' + next_url[1] + "/" + next_url[2] + '.html'
            # print(article)
            yield Request(article, callback=self.parse_news)

    def parse_news(self, response):
        item = TencentItem()
        selector = Selector(response)
        url_pattern2 = r'(\w+)://(\w+)\.qq\.com/(\w+)/(\d{8})/(\w+)\.html'
        pattern = re.match(url_pattern2, str(response.url))
        print(pattern)

        source = 'tencent'
        date = pattern.group(4)
        newsId = pattern.group(5)

        # res = requests.get(response.url)
        print(response.text)
        cmtid = re.findall(re.compile(r'"comment_id": "(\d+)"'),str(response.text))
        title = re.findall(re.compile(r'"title": "(.*)"'),str(response.text))
        print('cmt'+ str(cmtid[0]))
        comments = 'http://coral.qq.com/'+cmtid[0]
        passage = re.findall(re.compile(r'<p class="one-p">(.*)</p>'),str(response.text))
        res_str = ''
        for every_pas in passage:
            res_str+=every_pas

        print(res_str)

        # print('title'+ str(title[0]))

        item['source'] = source
        item['date'] = date
        item['newsId'] = newsId
        item['comments'] = {'link': comments}
        item['contents'] = {'link': str(response.url), 'title': u'', 'passage': u''}
        item['contents']['title'] = str(title[0])
        item['contents']['passage'] = res_str
        # print("-------------------------------")
        # print(date)
        # print(newsId)
        # print("-------------------------------")
        yield item


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

