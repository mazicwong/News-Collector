# coding=utf-8


import os
# return : python_path = '/home/mazic/anaconda3/bin/python'
python_path = os.popen("which python").readline() # 适应不同主机环境
python_path = python_path.strip()


'''
    don't use "os.system('python runsegment.py')" because it will use python2.7
    directly use /home/xxx/python3.6 instead
'''

main_path = os.popen("pwd").readline().strip()
path_res = os.path.join(main_path, '../result ')
path_tencent = os.path.join(main_path, '../news_crawl/docs/tencent ')
path_netease = os.path.join(main_path, '../news_crawl/docs/netease ')
path_sina = os.path.join(main_path, '../news_crawl/docs/sina ')


os.system(python_path + " categorize.py -o " + path_res +
          path_tencent + path_netease + path_sina)

'''
getabstract.py:  第一轮数据清洗: 正文,取词比例,取句子比例
    GetPassageAbstract(passage, 0.4, 0.3)


categorize.py:
    usage:  python categorize.py -k number_of_tags -o output_dir source_dir1 source_dir2 source_dir3 ...
'''


'''
TO DO : 
I find a question that is if you write "os.system('python runsegment.py')", then you use python 2.7
while if you use "scrapy.cmdline('python runsegment.py')", then you use python 3.6 just as what I set the system's default env
Why ???
'''