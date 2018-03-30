#!/usr/bin/env python
# coding=utf-8

# buildvectors.py
from segment.basicfuncs import TrimSpaces

import jieba
import jieba.posseg as pseg

'''
函数接口: GetPassageAbstract(passage, 0.4, 0.3)
传入: 正文,取词比例,取句子比例
返回: 剔除含有关键词较少的句子后的正文(如删去"扫一扫获取公众号"等)

- 依赖:  需要/user_dicts中的'sentencesegmtdict.txt': 判断句子结束的符号
        需要/user_dicts中的'elmnatrredict.txt': 定义所要取的词的词性
- Python Console中调试时,测试路径 os.chdir('要设置的当前目录')    os.getcwd()
'''

#以下: 得到elmn_dict字典,存储elmnattrdict中的词性与权值
USER_DICTS_PATH = '../segment/user_dicts' #在website中调用就要改
if __name__ == '__main__':
    USER_DICTS_PATH = 'user_dicts'
elmn_dict = {}
f = open(USER_DICTS_PATH + '/elmnattrdict.txt', 'r')
lines = f.readlines()  # 得到一个存每行文本的列表
f.close()
for line in lines:     # 每行文本做映射
    item = line.split()
    elmn_dict[item[0]] = int(item[1])
# print(elmn_dict)




# 以下: 定义接下来处理的数据结构
# 得到一个segmt_list的列表,来自存放在sentencesegmtdict.txt中的`所有符号+换行`
class Sentence():
    f = open(USER_DICTS_PATH + '/sentencesegmtdict.txt', 'r')
    segmt_list = [x[:-1] for x in f.readlines()]
    segmt_list.append('\n')
    f.close()

    def __init__(self, content, weight=0):
        self.content = content
        self.weight = float(weight)


# GetPassageAbstract(passage, 0.4, 0.3)
# 主函数: 传入正文,取词比例,取句子比例
def GetPassageAbstract(passage, keys_factor=0.5, sentences_factor=0.8, join_character=''):
    if keys_factor <= 0 or keys_factor > 1:
        print("Error: keys_factor: " + str(keys_factor) + " illegal, corrected to 0.5")
        keys_factor = 0.5
    if sentences_factor <= 0 or sentences_factor > 1:
        print('Error: sentences_factor: ' + str(sentences_factor) + ' illegal, corrected to 0.8')
        sentences_factor = 0.8
    passage = TrimSpaces(passage)  # 子函数0: 去掉正文前导和后导的连续空格换行等
    sentences = GetPassageSentences(passage)  # 子函数1: 按照"!?.\n"将正文分为多个句子,自定义为sentences={content-weight}类型
    tags = GetPassageTags(passage, keys_factor)  # 子函数2: 得到正文分词后按词频降序排的列表tags=['网民','沙漠'...]
    return GetAbstract(sentences, tags, sentences_factor, join_character) # 子函数3: 按`取句子比例`剔除包含关键词很少的句子



# debug函数,输出Sentences类型
def PRINT(s):
    for ss in s:
        print(ss.content, ss.weight)


# 子函数1:将文本切割为sentences={content-weight}类型的多个句子
# return {'今天去了板障山': 1, '今天很开心': 1, '中国发射了火箭': 1}
def GetPassageSentences(passage):
    text = passage  # unicode(passage, 'utf-8')
    sentences = []
    index = 0
    i = 0
    for i in range(0, len(text)):
        if text[i] in Sentence.segmt_list:
            sentences.append(Sentence(text[index:i + 1]))
            index = i + 1
    if index != i:
        sentences.append(Sentence(text[index:i]))
    # PRINT(sentences)
    return sentences


# 子函数2: 返回传入文本进行分词后的词组成的列表,按词频权重从大到小排;keys_factor是返回词数占所有词的比例,keys_factor=1就是取所有的词
# return ['案发', '距离', '已经', '是', '公园']
def GetPassageTags(passage, keys_factor):
    # 1. 通过jieba对传入的文本进行分词与词性标注,得到每个词对应权重tags={key-weight}
    words = pseg.cut(passage)  # 词性标注,返回generator={word,flag},比如 "分析 v, 天安门 n"
    tags = {}
    for word, flag in words:
        # print(word.word, word.flag)
        if tags.get(word) != None:      # 前面存过该词就加1
            tags[word] += 1
            continue
        if elmn_dict.get(flag) != None: # 不存在该词,但词性是要的(elmnatrrdict.txt),就存下,先用get判是因为直接取flag可能异常
            if elmn_dict[flag] != 0:    # '0':
                tags[word] = 1
        elif elmn_dict.get(flag[0] + '*') != None:
            if elmn_dict[flag[0] + '*'] != 0:  # '0':
                tags[word] = 1
        else:
            print('Warning: word: ' + word, flag[0] + ' attr not seen, counted')
            tags[word] = 1

    # 2. 处理上面得到的tags={key-weight}字典
    # 首先将该字典转换为列表,并对第二个属性`词权重`进行降序排列,最后返回权重从大到小排的字典
    lst = []
    for k, v in tags.items():
        lst.append([k, v])
    lst = sorted(lst, key=lambda x:x[1], reverse=True)
    return [tag[0] for tag in lst[0:max(1, int(round(len(lst) * keys_factor)))]]



# 子函数3: 传入`句子,词,取句子比例,句子连接符`,返回剔除与原文关键词无关的句子(如微信扫一扫之类的)
def GetAbstract(sentences, tags, sentences_factor, join_character=''):
    # 按照关键词给句子分配权重,找到含有关键词最多的句子
    tags_set = set(tags)
    for sentence in sentences:
        words = list(jieba.cut(sentence.content))
        for word in words:
            if word in tags_set:
                sentence.weight += 1.0 / len(words)
    # PRINT(sentences)
    result = sorted(sentences, key=lambda s: s.weight, reverse=True)
    # PRINT(result)

    # 取句子比例
    thresh_index = int(min((round(len(sentences) * sentences_factor), len(sentences) - 1)))
    if thresh_index < 0 or thresh_index >= len(result):
        return ''
    thresh = result[thresh_index].weight
    ans = ['']
    for sentence in sentences:
        if sentence.weight > 0 and sentence.weight > thresh:
            ans.append(sentence.content)
    return join_character.join(ans)