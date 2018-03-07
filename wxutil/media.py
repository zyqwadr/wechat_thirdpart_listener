# -*- coding: utf-8 -*-
# filename: media.py
import urllib2

import poster.encode
from poster.streaminghttp import register_openers

from wxutil.basic import Basic


class Media(object):
    def __init__(self):
        register_openers()
    #上传图片
    def uplaod(self, accessToken, filePath, mediaType):
        openFile = open(filePath, "rb")
        param = {'media': openFile}
        postData, postHeaders = poster.encode.multipart_encode(param)

        postUrl = "https://api.weixin.qq.com/cgi-bin/media/upload?access_token=%s&type=%s" % (accessToken, mediaType)
        request = urllib2.Request(postUrl, postData, postHeaders)
        urlResp = urllib2.urlopen(request)
        print urlResp.read()

    def get(self, accessToken, mediaId):
        postUrl = "https://api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s" % (accessToken, mediaId)
        urlResp = urllib2.urlopen(postUrl)

        headers = urlResp.info().__dict__['headers']
        if ('Content-Type: application/json\r\n' in headers) or ('Content-Type: text/plain\r\n' in headers):
            jsonDict = json.loads(urlResp.read())
            print jsonDict
        else:
            buffer = urlResp.read()  # 素材的二进制
            mediaFile = file("test_media.jpg", "wb")
            mediaFile.write(buffer)
            print "get successful"

# 上传临时素材
if __name__ == '__main__':
    myMedia = Media()
    accessToken = Basic().get_access_token()
    filePath = "/Users/yangweijie/Desktop/adf.png"   #请安实际填写
    mediaType = "image"
    myMedia.uplaod(accessToken, filePath, mediaType)


#  下载临时素材
# if __name__ == '__main__':
#     myMedia = Media()
#     accessToken = Basic().get_access_token()
#     mediaId = "PR4FabjKA6JWLLsQN6VPz_CrW72I_nbXiOYGA5pdz4UeGAAV4qPHXH6BaSKKzccD"
#     myMedia.get(accessToken, mediaId)