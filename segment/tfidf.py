# coding=utf-8

from basicfuncs import IsFile

import json
import jieba

# 评估某一关键词对文本的重要程度


# 子函数1: 给关键词和文本,统计出关键词tags=[]的词频,返回对应字典
def GetTermFreqFromContent(tags, content):
    """

    :param tags: 输入关键词
    :param content: 输入文本内容
    :return: 表示统计词频,返回字典{'新疆': 1, '网民': 7}
    """
    tfdict = {}
    for tag in tags:
        tfdict[tag] = 0

    seg_list = jieba.cut(content)
    has_words = False
    for word in seg_list:
        if word in tfdict:
            tfdict[word] = tfdict[word] + 1
            has_words = True

    if has_words:
        return tfdict
    else:
        return None

# 主函数: 给关键词和文本路径,统计出关键词tags=[]的词频,返回对应字典
def GetTermFreqFromFile(tags, file_path):
    if not IsFile(file_path):
        print(file_path + " not exists or not a file, can't get TF")
        return None
    f = open(file_path, 'r')
    js = json.load(f)
    passage = js['contents']['passage']
    f.close()
    return GetTermFreqFromContent(tags, passage)

# print(GetTermFreqFromFile(['新疆','网民'], './TEST/000913.json'))