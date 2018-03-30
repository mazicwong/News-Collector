#!/usr/bin/env python
# coding=utf-8

# basicfuncs.py
import math
import os
import time




def ADtimeToTimestamp(time_str, time_format, length = 10):
    if time_str == None:
        return None
    return str(time.mktime(time.strptime(time_str, time_format)))[:length]




def MakeDirectory(dir_path):
    if not IsDirectory(dir_path):
        os.makedirs(dir_path)

def CopyFile(source_file, target_dir):
    os.system("cp %s %s" % (source_file, target_dir))



# 子函数1: (vec1*vec2)/sqrt(vec1^2+vec2^2)
def CosinSimilarity(vector1, vector2):
    if len(vector1) != len(vector2):
        print("Error: vector1:" + vector1 + " and vector2: " + vector2 + "have different dimensions")
        return None

    numerator = 0.0
    v1_square = 0.0
    v2_square = 0.0
    for i in range(0, len(vector1)):
        numerator += vector1[i] * vector2[i]
        v1_square += vector1[i] * vector1[i]
        v2_square += vector2[i] * vector2[i]
    denominator = math.sqrt(v1_square * v2_square)
    if denominator == 0:
        return None
    else:
        return numerator / denominator

# 主函数: 用来计算两个关键词字典的cos距离(findsimilarpassage.py)
def CosinSimilarityForDict(dict1, dict2):
    if len(list(dict1.keys())) != len(list(dict2.keys())):
        print("Error: dict1: " + str(dict1.keys()) + " and dict2: " + str(dict2.keys()) + "have different key numbers")
        return None
    vector1 = [] # 权重向量
    vector2 = []
    for key in list(dict1.keys()):
        if key not in dict2:
            print("Error: key: " + key + " not exists in dict2")
            return None
        vector1.append(dict1[key])
        vector2.append(dict2[key])
    return CosinSimilarity(vector1, vector2)


def GetTimestamp(length):
    return str(time.time())[:length]


# exists检验路径/文件是否存在, isfile检验是否为文件
def IsDirectory(dir_path):
    if not os.path.exists(dir_path):
        return False
    elif os.path.isfile(dir_path):
        return False
    else:
        return True

def IsFile(file_path):
    if not os.path.exists(file_path):
        return False
    elif not os.path.isfile(file_path):
        return False
    else:
        return True





def TimestampToADtime(timestamp, time_format = '%Y-%m-%d %H:%M:%S'):
    return str(time.strftime(time_format, time.localtime(float(timestamp))))


# 去掉前导和后导的连续空格换行等(getabstract.py)
def TrimSpaces(text):
    lst = [' ', '\t', '\n', '\r']
    front_index = 0
    for i in range(0, len(text)):
        if text[i] in lst:
            front_index += 1
        else:
            break
    text = text[front_index:]    # 去掉前导空格等
    tail_index = len(text) - 1
    for i in range(tail_index, 0, -1):
        if text[i] in lst:
            tail_index -= 1
        else:
            break
    text = text[0:tail_index]    # 去掉后导空格等
    return text


