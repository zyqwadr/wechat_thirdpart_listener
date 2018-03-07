# -*- coding: utf-8 -*-
# filename: 调用图灵机器人api

import urllib2
import json
import globalvar as gl
import traceback

# 正确返回：{u'emotion': {u'userEmotion': {u'a': 0, u'emotionId': 0, u'd': 0, u'p': 0}, u'robotEmotion': {u'a': 0, u'emotionId': 0, u'd': 0, u'p': 0}}, u'intent': {u'actionName': u'', u'code': 10004, u'intentName': u''}, u'results': [{u'groupType': 1, u'resultType': u'text', u'values': {u'text': u'\u58eb\u5927\u592b\u80fd\u597d\u6253\u53d1\u5417\uff1f'}}]}
# 超过次数返回：{u'intent': {u'code': 4003}}

postUrl = ("http://openapi.tuling123.com/openapi/api/v2")

def replyTextMsg(content, userId):
    userId = abs(hash(userId))
    try:
        postData = (
        "{\"reqType\": %d,\"perception\": {\"inputText\": {\"text\": \"%s\"}},\"userInfo\": {\"apiKey\": \"%s\",\"userId\": \"%s\"}}"
        % (0, content, getApiKey(userId), userId))
        # print(postData)
        gl.getLogger().debug("tuling req:"+postData)
        urlResp = urllib2.urlopen(postUrl, postData)
        jsonDict = json.loads(urlResp.read(), encoding='utf-8')
        # print(jsonDict)
        for result in jsonDict['results']:
            if result['resultType'] == 'text':
                return result['values']['text']
        return None
    except Exception:
        gl.getLogger().error(traceback.format_exc())
        return None

def replyImgMsg(picUrl, userId):
    userId = abs(hash(userId))
    postData = (
    "{\"reqType\": %d,\"perception\": {\"inputImage\": {\"text\": \"%s\"}},\"userInfo\": {\"apiKey\": \"%s\",\"userId\": \"%s\"}}"
    % (1, picUrl, getApiKey(userId), userId))
    # print(postData)
    urlResp = urllib2.urlopen(postUrl, postData)
    jsonDict = json.loads(urlResp.read())
    # print(jsonDict)
    for result in jsonDict['results']:
        if result['resultType'] == 'text':
            answer = result['values']['text']
            print(answer)
        if result['resultType'] == 'url':
            answer = result['values']['url']
            print(answer)
    return answer

# 每个apikey限制调用1000次
def getApiKey(userId):
    try:
        apiKeys = gl.get_value('config')['tuling_apikeys']
        apiKeyCount = len(apiKeys)
        index = 0
        if apiKeyCount > 1:
            index = userId % apiKeyCount
        apikey = apiKeys[index]
        return str(apikey)
    except Exception:
        return 'f4693d84da394394825b115e0364ce17'


# 限制每个微信号每天最多与图灵机器人聊天100次
def userChatLimit(userId):
    print()



if __name__ == '__main__':
    for i in range(10):
        print(replyImgMsg("http://mmbiz.qpic.cn/mmbiz_jpg/tiarshdD1CdMBeTyDfPHlLBgia5F222QGNSQY33iaickrRib2xI7vT5RFWialicEP0qDeFhZib6fNfEJ84pOLniaN3WjFgw/0","o1WJfvzosqiksDTidxM4") )