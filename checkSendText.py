# -*- coding: utf-8 -*-

import urllib2
import json

def checkSendText(authorization_code):
    getUrl = "http://www.d.intbee.com/componentlogin/wechat/component_access_token"
    request = urllib2.Request(getUrl)
    urlResp = urllib2.urlopen(request)
    urlResp = json.loads(urlResp.read())
    c_access_token = urlResp['result']['component_access_token']
    print(urlResp['result']['component_access_token'])

    postUrl = "https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token=%s" % c_access_token
    print(postUrl)
    postData = "{ \"component_appid\": \"%s\",\"authorization_code\": \"%s\" }" % (
    'wxfcaaaab9c2865a56', authorization_code)
    urlResp = urllib2.urlopen(postUrl, postData)
    urlResp = json.loads(urlResp.read())
    print(urlResp)


def send(openid, access_token,content):
    postUrl = "https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s" % access_token
    print(postUrl)
    postData = "{ \"touser\": \"%s\",\"msgtype\": \"text\",\"text\":{\"content\":\"%s\"} }" % (openid, content)
    print(postData)
    urlResp = urllib2.urlopen(postUrl, postData)
    urlResp = json.loads(urlResp.read())
    print(urlResp)


if __name__ == '__main__':
    authorization_code = 'queryauthcode@@@8ujpm7hf8SNkKtD6a1U167ES16J1nvNsnIvWkDyH3vCRekP-vGARidwb7hHMDRVZvVHJto1kvTPg_WX-EM5HSQ'
    checkSendText(authorization_code)

    # openid = "ozy4qt5QUADNXORxCVipKMV9dss0"
    # access_token = ""
    # content = authorization_code + '_from_api'
    # send(openid,access_token,content)



