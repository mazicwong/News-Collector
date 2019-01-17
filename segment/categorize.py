# coding=utf-8

# categorize.py
from optparse import OptionParser
from basicfuncs import IsDirectory, MakeDirectory, CopyFile
from findsimilarpassage import FindSimilarPassageFromSet
from tfidf import GetTermFreqFromFile
from extracttags import ExtractTagsFromFile

import json
import os
import re
import sys
import time

# 输入:新闻来源,输出地址,标签数(默认10)
# 输出:
def Categorize(source_dirs, output_dir, num_of_tags):
    if not IsDirectory(output_dir):
        print("output_dir not exists or not a directory")
        sys.exit(3)

    source_sets = source_dirs # Set(source_dirs) # will disrupt the original order

    # 1. 从给定路径获取所有的新闻json地址,存入news_sets=[{tencent1,tencent2},{netease1,netease2},{sina1,sina2}]中
    news_sets = [] # a list of sets
    for source_dir in source_sets:
        if not IsDirectory(source_dir):
            print("Error. source_dir: " + source_dir + " not exists or not a directory")
            continue
        else:
            tmp_set = set([])
            for parent, dir_names, file_names in os.walk(source_dir):  # os.walk遍历该目录,返回三元组{当前文件夹路径,当前文件夹中文件夹,当前文件夹中文件}
                pattern = re.match(r'.*/([0-9]{8})[/]{,1}$', parent)
                if pattern != None and os.stat(parent).st_mtime < last_mtime: # 文件上次修改时间<系统上次启动时间,则说明已更新过
                    print('Directory: ' + parent + ' is too old, skipped')
                    continue
                for file_name in file_names:
                    if file_name[-4:] == 'json' and os.stat(parent + '/' + file_name).st_mtime >= last_mtime:
                        tmp_set.add(parent + '/' + file_name)
            news_sets.append(tmp_set)

    # 2. 找到所有文本的相似文本,有的话就存放到/result
    for i in range(0, len(news_sets) - 1):
        for file_path in news_sets[i]:
            file_name = re.match(r".*/([-\w]+\.json)", file_path).group(1) # 提取出文件名,'025453.json'
            print("---------------------------------")
            print("Searching for " + file_name + "'s similar passages ...")

            tags = ExtractTagsFromFile(file_path, num_of_tags)  # 子函数1: 传入文件和词数,返回前几个关键词tags=['','','']
            example_tf = GetTermFreqFromFile(tags, file_path)   # 子函数2: 传入关键词和文件,用tfidf返回对应词与权重example_tf={'':12, '':8}
            if example_tf == None:
                continue
            for j in range(i + 1, len(news_sets)):
                resfile = FindSimilarPassageFromSet(news_sets[j], example_tf)  # 子函数3: 从其他平台新闻集找到相似文章,返回相似文件路径
                if resfile == None:
                    #print "No similar passage to " + file_name + " in "
                    continue
                else:
                    f = open(file_path, 'r')
                    js = json.load(f)
                    date = js['date']
                    newsId = js['newsId']
                    f.close()

                    result_path = output_dir + '/' + date + '/' + newsId + '/'
                    MakeDirectory(result_path)

                    if not os.path.exists(result_path + '/' + file_name):
                        CopyFile(file_path, result_path)
                    CopyFile(resfile, result_path)
                    print("found similar passage to " + file_name + ": " + resfile)





USAGE = "usage: python categorize.py [-k number_of_tags] [-o output_directory] [source_directories ...]"
parser = OptionParser(USAGE)
parser.add_option("-k", dest="number_of_tags", help="the number of tags to be extracted from the passage")
parser.add_option("-o", dest="output_dir", help="the directory in which the results are stored")

(opt, args) = parser.parse_args()

# 调试: 模拟命令行输入
# args = ["-k","3", "-o", "aaa", "bbb" ,"ccc"]
# (opt, args) = parser.parse_args(args)   # opt.num_of_tags=3; opt.output_directory="aaa"; args=["bbb","ccc"];



if opt.output_dir is None or len(args) < 2:
    print(USAGE)
    sys.exit(1)

if opt.number_of_tags is not None and opt.number_of_tags >= '1':
    num_of_tags = opt.number_of_tags
else:
    num_of_tags = 10

output_dir = opt.output_dir
source_dirs = args

f = open(os.path.join(output_dir, 'magicnumber'), 'r')  # 1970/1/1开始的时间戳,按秒偏移
timestamp = f.read()
last_mtime = int(re.match('([0-9]{10}).*', timestamp).group(1))  # 上次系统启动的时间
f.close()
OldestDir = time.strftime('%Y%m%d', time.localtime(float(timestamp)))

Categorize(source_dirs, output_dir, num_of_tags)

timestamp = str(time.time())
f = open(os.path.join(output_dir, 'magicnumber'), 'w')
f.write(timestamp)
f.close()
