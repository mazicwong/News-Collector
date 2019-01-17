# coding=utf-8


import os
python_path = '/home/mazic/anaconda3/bin/python'

'''
    don't use "os.system('python run.py')" for the use of python2.7
    use /home/xxx/python3.6 instead
'''

os.system(python_path + " categorize.py -o /home/mazic/tmp/news/result "
          "/home/mazic/tmp/news/news_crawl/docs/tencent "
          "/home/mazic/tmp/news/news_crawl/docs/netease "
          "/home/mazic/tmp/news/news_crawl/docs/sina")


'''
getabstract.py:  第一轮数据清洗: 正文,取词比例,取句子比例
    GetPassageAbstract(passage, 0.4, 0.3)


categorize.py:
    usage:  python categorize.py -k number_of_tags -o output_dir source_dir1 source_dir2 source_dir3 ...
'''


'''
TO DO : 
I find a question that is if you write "os.system('python run.py')", then you use python 2.7
while if you use "scrapy.cmdline('python run.py')", then you use python 3.6 just as what I set the system's default
But Why ???
'''