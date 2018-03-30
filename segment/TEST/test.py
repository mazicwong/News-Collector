#!/usr/bin/env python
# coding=utf-8

import os
import json
from getabstract import GetPassageAbstract

f = open('000913.json', 'r')
js = json.load(f)
passage = js['contents']['passage']
print(GetPassageAbstract(passage, 0.4, 0.3)) # 第一轮数据清洗: 正文,取词比例,取句子比例



'''
json 文件包含 {}
cmtId:
date:
comments: {link:}
source:
newsId:
contents: {passage:   link:   title:}
'''
