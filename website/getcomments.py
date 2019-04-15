# getcomments.py
import http.client
import json
import re
import sys
sys.path.append('../segment')

from basicfuncs import ADtimeToTimestamp, GetTimestamp

def GetComments(para_dict):
    source = para_dict.get('source')
    if source == 'tencent':
        return GetCommentsFromTencent(para_dict)
    elif source == 'netease':
        return GetCommentsFromNetease(para_dict)
    elif source == 'sina':
        return GetCommentsFromSina(para_dict)
    else:
        return None

def GetCommentsFromTencent(para_dict): # currently hot comments
    domain = 'coral.qq.com'
    req = '/article/%s/hotcomment?reqnum=%s&callback=myHotcommentList&_=%s%s' % (para_dict.get('cmtId'), para_dict.get('reqNum', '10'), GetTimestamp(10), '444')
    data = re.match(r'^myHotcommentList\((.*)\)', GetDataFromHttp(domain, req)).group(1)
    js = StrToJson(data)
    path_dict = {'source':'tencent', 'prefix':['data', 'commentid'], 'user':['userinfo', 'nick'], 'time':['time'], 'content':['content']}
    return ReformatComments(js, path_dict)

def GetCommentsFromNetease(para_dict): # currently hot comments
    # http://comment.news.163.com/news_shehui7_bbs/ECQFVO1I00018AOR.html
    # http://comment.tie.163.com/ECQIS5360001875P.html
    domain = 'comment.tie.163.com'
    # req = '/news_shehui7_bbs/%s.html' % para_dict.get('cmtId') (要处理动态的..)
    # req = '/data/%s/df/%s_1.html' % (para_dict.get('boardId'), para_dict.get('cmtId'))
    req = '/%s.html' % para_dict.get('cmtId')
    data = str(GetDataFromHttp(domain, req), 'utf-8')#.encode('gbk')
    print("******************================")
    print(data)
    print("******************================")
    data = re.match(r'^var \w+=({.*});$', data).group(1)
    js = StrToJson(data)
    path_dict = {'source':'netease', 'prefix':['hotPosts'], 'user':['1', 'n'], 'time': ['1', 't'], 'content': ['1', 'b']}
    return ReformatComments(js, path_dict, ADtimeToTimestamp, '%Y-%m-%d %H:%M:%S')

def GetCommentsFromSina(para_dict):
    domain = 'comment5.news.sina.com.cn'
    req = '/page/info?format=%s&channel=%s&newsid=%s&group=%s&compress=1&ie=gbk&oe=gbk&page=%s&page_size=%s&jsvar=requestId_%s' % (para_dict.get('format', 'json'), para_dict.get('channelId'), para_dict.get('cmtId'), para_dict.get('group', '0'), para_dict.get('page', '1'), para_dict.get('pageSize', '100'), para_dict.get('requestId', '444'))
    data = str(GetDataFromHttp(domain, req), 'gbk')
    js = StrToJson(data)
    path_dict = {'source':'sina', 'prefix':['result', 'hot_list'], 'user':['nick'], 'time':['time'], 'content':['content']}
    return ReformatComments(js, path_dict, ADtimeToTimestamp, '%Y-%m-%d %H:%M:%S')

def GetDataFromHttp(domain, req):
    conn = http.client.HTTPConnection(domain)
    conn.request('GET', req)
    resp = conn.getresponse()
    data = None
    if not (resp.status == 200 and  (resp.reason == 'OK' or resp.reason == 'ok')):
        print('Error: Get response from ' + domain + req + ' failed')
    else:
        print('Got data from ' + domain + req)
        data = resp.read()
    conn.close()
    return data

def ReformatComments(js, path_dict, time_conversion_func = None, time_conversion_args = None):
    comments_list = []
    comments = js
    for key in path_dict['prefix']:
        comments = comments[key]

    if comments is not None:
        for comment in comments:
            new_comment = {'source':path_dict['source'], 'user': comment, 'time':comment, 'content':comment}
            # get content
            for key in path_dict['content']:
                new_comment['content'] = new_comment['content'].get(key)
            
            # get time
            for key in path_dict['time']:
                new_comment['time'] = new_comment['time'].get(key)

            # get user
            for key in path_dict['user']:
                new_comment['user'] = new_comment['user'].get(key)

            if new_comment['user'] == None or new_comment['time'] == None or new_comment['content'] == None:
                continue

            # convert time to timestamp
            if time_conversion_func != None:
                new_comment['time'] = time_conversion_func(str(new_comment['time']), time_conversion_args)

            comments_list.append(new_comment)

    return comments_list

def StrToJson(data):
    return json.loads(data)
