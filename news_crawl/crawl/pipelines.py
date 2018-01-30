# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import codecs

class CrawlPipeline(object):
    def __init__(self):
        self.current_dir = os.getcwd()

    def process_item(self, item, spider):
        dir_path = self.current_dir + '/docs/' + item['source'] + '/' + item['date']
        print(dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        news_file_path = dir_path + '/' + item['newsId'] + '.json'
        if os.path.exists(news_file_path) and os.path.isfile(news_file_path):
            print("*****************************")
            print(item['newsId'] + '.json exists, just skip')
            print("*****************************")
        
        news_file = codecs.open(news_file_path, 'w', 'utf-8')
        line = json.dumps(dict(item))
        news_file.write(line)
        news_file.close()
        return item
