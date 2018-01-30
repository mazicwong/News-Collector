#!/usr/bin/env python
# coding=utf-8

import scrapy
import re
from scrapy.selector import Selector
from crawl.items import NeteaseItem,TencentItem,SinaItem
from scrapy.http import Request
from urllib.request import urlopen
from crawl.maziclib.news_fun import ListCombiner


class NeteaseNewsSpider(scrapy.Spider):
    name = 'netease_news_spider'  #最后要调用的名字
    start_urls = ['http://news.163.com']
    allowed_domains = ['news.163.com']

    url_pattern = r'(http://news\.163\.com)/(\d{2})/(\d{4})/(\d+)/(\w+)\.html'

    def parse(self, response):  # response即网页数据
        pat = re.compile(self.url_pattern)
        next_urls = re.findall(pat, str(response.body))

        ###debug
        #article = next_urls[0][0]+'/'+next_urls[0][1]+'/'+next_urls[0][2]+'/'+next_urls[0][3]+'/'+next_urls[0][4]+'.html'
        #yield Request(article, callback=self.parse_news)
        ###debug

        for next_url in next_urls:
            article = next_url[0]+'/'+next_url[1]+'/'+next_url[2]+'/'+next_url[3]+'/'+next_url[4]+'.html'
            yield Request(article,callback=self.parse_news)

    def parse_news(self, response):
        item = NeteaseItem()
        selector = Selector(response)
        pattern = re.match(self.url_pattern, response.url)

        
        source = 'netease'
        date = '20'+pattern.group(2)+pattern.group(3)
        newsId = pattern.group(5)
        cmtId = pattern.group(5)
        
        productKey = re.findall(re.compile(r'"productKey" : "(\w+)"'), str(response.body))[0]
        comments_api = 'http://comment.news.163.com/api/v1/products/' + productKey + '/threads/' + newsId
        boardId = re.findall(r'"boardId":"(\w+)"',str(urlopen(comments_api).read()))[0]
        comments = ('http://comment.news.163.com/'+boardId+'/'+newsId+'.html')

        item['source'] = 'netease'
        item['date'] = date
        item['newsId'] = newsId
        item['cmtId'] = cmtId
        #item['boardId'] = boardId
        item['comments'] = {'link' : comments}
        item['contents'] = {'link' : str(response.url), 'title' : u'', 'passage' : u''}
        item['contents']['title'] = selector.xpath('//*[@id="epContentLeft"]/h1/text()').extract()
        item['contents']['passage'] = ListCombiner(selector.xpath('//*[@id="endText"]/p').extract())
        yield item




class TencentNewsSpider(scrapy.Spider):
    name = 'tencent_news_spider'  #最后要调用的名字
    start_urls = ['http://news.qq.com']
    allowed_domains = ['news.qq.com']

    #https://news.qq.com/a/20180120/000738.htm
    url_pattern = r'http://(\w+)\.qq\.com/a/(\d{8})/(\d+)\.htm'

    def parse(self, response):  # response即网页数据
        pat = re.compile(self.url_pattern)
        next_urls = re.findall(pat, str(response.body))

        ### debug
        #article = 'http://'+next_urls[0][0]+'.qq.com/a/'+next_urls[0][1]+'/'+next_urls[0][2]+'.htm'
        #print(article)
        #yield Request(article,callback=self.parse_news)
        ### debug

        for next_url in next_urls:
            article = 'http://'+next_url[0]+'.qq.com/a/'+next_url[1]+'/'+next_url[2]+'.htm'
            yield Request(article,callback=self.parse_news)
       

    def parse_news(self, response):
        item = TencentItem()
        selector = Selector(response)
        url_pattern2 = r'(\w+)://(\w+)\.qq\.com/a/(\d{8})/(\d+)\.htm'
        pattern = re.match(url_pattern2, str(response.url))
        
        source = 'tencent'
        date = pattern.group(3)
        newsId = pattern.group(4)
        cmtId = re.findall(re.compile(r'cmt_id = (\d+);'), str(response.body))[0]
        comments = 'http://coral.qq.com/' + cmtId


        item['source'] = source
        item['date'] = date
        item['newsId'] = newsId
        item['comments'] = {'link' : comments}
        item['contents'] = {'link' : str(response.url), 'title' : u'', 'passage' : u''}
        item['contents']['title'] = selector.xpath('//*[@id="Main-Article-QQ"]/div/div[1]/div[1]/div[1]/h1/text()').extract()
        item['contents']['passage'] = ListCombiner(selector.xpath('//*[@id="Cnt-Main-Article-QQ"]/p/text()').extract())  #这里要不要留下那些<tag>???(要不要/text()??)
        print("-------------------------------")
        print (date)
        print(newsId)
        print("-------------------------------")
        yield item


class SinaNewsSpider(scrapy.Spider):
    name = 'sina_news_spider'  #最后要调用的名字
    start_urls = ['http://news.sina.com.cn']
    allowed_domains = ['news.sina.com.cn']

    url_pattern = r'http://(\w+).sina.com.cn/(\w+)/(\w+)/(\d{4}-\d{2}-\d{2})/.+\.(?:s)html'

    def parse(self, response):  # response即网页数据
        pat = re.compile(self.url_pattern)
        next_urls = re.findall(pat, str(response.body))
        print(next_urls)
        print(len(next_urls))
        print(type(next_urls))

        ### debug
        #article = 'http://'+next_urls[0][0]+'.qq.com/a/'+next_urls[0][1]+'/'+next_urls[0][2]+'.htm'
        #print(article)
        #yield Request(article,callback=self.parse_news)
        ### debug

        #for next_url in next_urls:
        #    article = 'http://'+next_url[0]+'.qq.com/a/'+next_url[1]+'/'+next_url[2]+'.htm'
        #    yield Request(article,callback=self.parse_news)
       

    def parse_news(self, response):
        item = SinaItem()
        selector = Selector(response)
        pattern = re.match(self.url_pattern, str(response.url))

        item['source'] = 'sina'  # pattern.group(1)
        item['date'] = ListCombiner(str(pattern.group(2)).split('-'))
        item['newsId'] = sel.re(r'comment_id:(\d-\d-\d+)')[0]
        item['cmtId'] = item['newsId']
        item['channelId'] = sel.re(r'comment_channel:(\w+);')[0]
        item['comments'] = {'link': str(
            'http://comment5.news.sina.com.cn/comment/skin/default.html?channel=' + item['channelId'] + '&newsid=' +
            item['cmtId'])}
        item['contents'] = {'link': str(response.url), 'title': u'', 'passage': u''}
        item['contents']['title'] = sel.xpath("//h1[@id='artibodyTitle']/text()").extract()[0]
        item['contents']['passage'] = ListCombiner(sel.xpath('//p/text()').extract())
        yield item




