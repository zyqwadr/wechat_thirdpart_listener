# -*- coding: utf-8 -*-
# filename: handle.py
# 微信开放平台  覆盖现网检测  接入接口
# 参考 ： https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&id=open1419318611&token=&lang=zh_CN

import sys

import web

from wxmodel import reply, receive
from wxcrypt.WXBizMsgCrypt import WXBizMsgCrypt

reload(sys)
sys.setdefaultencoding('utf-8')

# 测试
# encodingAESKey = "c0fa1bc00531bd78ef38c628449c5102aeabd49b5dc"
# token = "c0fa1bc00531bd78ef38c628449c5102aeabd49b5dc3a2a516ea6ea959d6658e"
# appId = "wxfcaaaab9c2865a56"

# 正式
encodingAESKey = "c0fa1bc00531bd78ef38c628449c5102aeabd49b5dc"
token = "c0fa1bc00531bd78ef38c628449c5102aeabd49b5dc3a2a516ea6ea959d6658e"
appId = "wx1bc10a5bb83a43bb"


class ThirdPartHandle(object):
    def POST(self, appid):
        try:
            print(appid)
            input = web.input()
            print input
            webData = web.data()
            print webData
            decrypt_test = WXBizMsgCrypt(token, encodingAESKey, appId)
            ret, decryp_xml = decrypt_test.DecryptMsg(webData, str(input.msg_signature), str(input.timestamp), str(input.nonce))
            print ret,decryp_xml
            recMsg = receive.parse_xml(decryp_xml)
            print(recMsg)
            if isinstance(recMsg, receive.Msg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                if recMsg.MsgType == 'text':
                    msc = recMsg.Content
                    # Text 检测
                    if msc == 'TESTCOMPONENT_MSG_TYPE_TEXT':
                        content = 'TESTCOMPONENT_MSG_TYPE_TEXT_callback'
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        encryp_test = WXBizMsgCrypt(token, encodingAESKey, appId)
                        ret, encrypt_xml = encryp_test.EncryptMsg(replyMsg.send(), input.nonce)
                        print(encrypt_xml)
                        return encrypt_xml
                    # Text 检测
                    if 'QUERY_AUTH_CODE:' == msc[0:16]:
                        query_auth_code = msc[16:len(msc)]
                        print(query_auth_code)
                        content = query_auth_code + "_from_api";
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        encryp_test = WXBizMsgCrypt(token, encodingAESKey, appId)
                        ret, encrypt_xml = encryp_test.EncryptMsg(replyMsg.send(), input.nonce)
                        print(encrypt_xml)
                        return encrypt_xml
            # Event 检测
            if isinstance(recMsg, receive.EventMsg):
                toUser = recMsg.FromUserName
                fromUser = recMsg.ToUserName
                content = recMsg.Event + "from_callback"
                replyMsg = reply.TextMsg(toUser, fromUser, content)
                encryp_test = WXBizMsgCrypt(token, encodingAESKey, appId)
                ret, encrypt_xml = encryp_test.EncryptMsg(replyMsg.send(), input.nonce)
                print(encrypt_xml)
                return encrypt_xml
            print "暂且不处理"
            return reply.Msg().send()
        except Exception, Argment:
            return Argment
