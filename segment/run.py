#!/usr/bin/env python
# coding=utf-8


import os

os.system("python categorize.py -o /home/mazic/pp/PycharmStudy/crawl/news/result "
          "/home/mazic/Python_Study/crawl/news/news_crawl/docs/tencent "
          "/home/mazic/Python_Study/crawl/news/news_crawl/docs/netease "
          "/home/mazic/Python_Study/crawl/news/news_crawl/docs/sina")


'''
getabstract.py:  第一轮数据清洗: 正文,取词比例,取句子比例
    GetPassageAbstract(passage, 0.4, 0.3)




categorize.py:
    usage:  python categorize.py -k number_of_tags -o output_dir source_dir1 source_dir2 source_dir3 ...


'''
