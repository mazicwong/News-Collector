#!/usr/bin/env python
# coding=utf-8

# findsimilarpassage.py
from basicfuncs import IsDirectory, CosinSimilarityForDict
from tfidf import GetTermFreqFromFile
import heapq
import os

class SimilarPassage:
    def __init__(self, similarity, file_path):
        self.similarity = similarity
        self.file_path = file_path

    def __lt__(self, other):
        return self.similarity < other.similarity

    def __gt__(self, other):
        return self.similarity > other.similarity

    def Relevant(self):
        return self.similarity < -0.75

# 主函数: 给文本集和关键词,判断有无相似
def FindSimilarPassageFromSet(news_set, example_tf):
    heap = []
    tags = []
    for tag in list(example_tf.keys()):
        tags.append(tag)

    for file_path in news_set:
        tf = GetTermFreqFromFile(tags, file_path)  # 获取关键词的词频 tf={}
        if tf == None:
            continue
        similarity = CosinSimilarityForDict(example_tf, tf)
        if not similarity == None:
            heap.append(SimilarPassage(similarity * -1.0, file_path))

    heapq.heapify(heap)
    if len(heap) == 0:
        return None
    result = heapq.heappop(heap)
    if result.Relevant():
        print("Similarity: " + str(result.similarity))
        news_set.discard(result.file_path)
        return result.file_path
    else:
        return None



# 备用的
def FindSimilarPassageFromDirectory(source_dir, example_tf):
    if not IsDirectory(source_dir):
        print("In findsimilarpassagefromdirectory: " + source_dir + " not exists or not a directory")
        return None

    heap = []
    tags = []
    for tag in list(example_tf.keys()):
        tags.append(tag)

    for parent, dir_names, file_names in os.walk(source_dir):
        for file_name in file_names:
            if file_name[-4:] == 'json':
                file_path = parent + '/' + file_name
                tf = GetTermFreqFromFile(tags, file_path)
                if tf == None:
                    continue
                similarity = CosinSimilarityForDict(example_tf, tf)
                if not similarity == None:
                    heap.append(SimilarPassage(similarity * -1.0, file_path))

    heapq.heapify(heap)
    if len(heap) == 0:
        return None
    result = heapq.heappop(heap)
    if result.Relevant():
        print("Similarity: " + str(result.similarity))
        return result.file_path
    else:
        return None

