# datastructures.py
import codecs
import json
import os
import sys
sys.path.append('../segment')

from basicfuncs import IsDirectory, IsFile

class News():
    def __init__(self, parent_dir, dir_name):
        self.parent_dir = parent_dir
        self.dir_name = dir_name
        self.title = ""
        self.file_paths = []
        self.sources = []

    def init_object(self):
        if len(self.title) == 0:
            current_path = os.path.join(self.parent_dir, self.dir_name)
            for file_name in os.listdir(current_path):
                file_path = os.path.join(current_path, file_name)
                if IsFile(file_path) and file_name[-4:] == 'json':
                    self.file_paths.append(file_path)
                    f = codecs.open(file_path, 'r', 'utf-8')
                    js = json.load(f)
                    f.close()
                    if len(self.title) == 0:
                        self.title = js['contents']['title']
                    self.sources.append(js['source'])
    def __lt__(self, other):
        return len(self.sources) < len(other.sources)

    def __gt__(self, other):
        return len(self.sources) > len(other.sources)

class DateDir():
    def __init__(self, parent_dir, date):
        self.parent_dir = parent_dir
        self.date = date
        self.news = []

    def __lt__(self, other):
        return self.date < other.date

    def __gt__(self, other):
        return self.date > other.date

    def get_news(self):
        current_path = os.path.join(self.parent_dir, self.date)
        for news_dir in os.listdir(current_path):
            if IsDirectory(os.path.join(current_path,news_dir)):
                self.news.append(News(current_path, news_dir))
                self.news[-1].init_object()
#                print os.path.join(current_path, news_dir)
        self.news.sort(reverse = True)

