# temp.py
import codecs, json
import sys
from getcomments import GetComments
source = 'all'
para_dict = { 'tencent':{'source':'tencent', 'cmtId':'1004703995'}, 'netease':{'source':'netease', 'boardId':'news_guonei8_bbs', 'cmtId':'9IISVTCG0001124J'}, 'sina':{'source':'sina', 'cmtId':'1-1-29283928', 'channelId':'gn', 'boardId':'news_shehui7_bbs'} }

def get_comments(dictionary):
    if dictionary == None:
        print('Error arg dictionary: ' + dictionary)
        sys.exit(-1)
    js = json.dumps(GetComments(dictionary))
    f = open('test/' + dictionary['source'] + '.json', 'w')
    f.write(js)
    f.close()

if len(sys.argv) >= 2:
    get_comments(para_dict[sys.argv[1]])
else:
    for key in list(para_dict.keys()):
        get_comments(para_dict[key])

