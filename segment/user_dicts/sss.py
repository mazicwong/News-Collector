#!/usr/bin/env python
# coding=utf-8

#encoding=utf-8

import sys, os
def w(f, content):
    f.write(content+'\n')

f = open('sentencesegmtdict.txt', 'w')
w(f, '!')
w(f, '?')
w(f, '.')
w(f, '。')
w(f,'！')
w(f,'？')
f.close()
