# coding=utf-8

# extracttags.py
from basicfuncs import IsDirectory, IsFile
import jieba
import jieba.analyse
import json
import os
import sys


# 提取文本关键词

def WriteTagsToFile(file_path, tags, encoding):
    print('\t'.join(tags))
    f_tag = open(file_path, 'w')
    f_tag.write('\t'.join(tags))
    f_tag.close()

# 子函数1: 从一段文本中抽取出关键词
def ExtractTagsFromContent(content, num_of_tags):
    tags = jieba.analyse.extract_tags(content, topK = num_of_tags)
    return tags


# 主函数: 从一个文件'025453.json'中提取正文的标签
def ExtractTagsFromFile(file_path, num_of_tags):
    """

    :param file_path: 输入文章路径
    :param num_of_tags: 输入关键词个数
    :return: 返回文章关键词
    """
    # print 'Extracting from ' + file_path + ' ...'
    if not IsFile(file_path):
        print("Path not exists or not a file")
        sys.exit(2)
    f = open(file_path, 'r')
    js = json.load(f)
    content = js['contents']['passage'] # f.read()
    tags = ExtractTagsFromContent(content, num_of_tags) # jieba.analyse.extract_tags(content, topK = num_of_tags)
    f.close()
    return tags

# print(ExtractTagsFromFile('./TEST/000913.json', 10))

# 备用的...(遍历文件夹下所有文章,输入关键词)
def ExtractTagsFromDirectory(dir_path, num_of_tags):
    if not IsDirectory(dir_path):
        print("Path not exists or not a directory")
        sys.exit(3)
    for parent, dir_names, file_names in os.walk(dir_path):
        for file_name in file_names:
            if file_name[-4:] == 'json':
                file_path = parent + '/' + file_name
                tags = ExtractTagsFromFile(file_path, num_of_tags)
                WriteTagsToFile(file_path[:-5] + '.tags', tags, 'utf-8')
