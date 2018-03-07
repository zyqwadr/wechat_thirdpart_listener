# -*- coding: utf-8 -*-
# filename: handle.py

import sys

import web
import json
import globalvar as gl
from chatbot import tulingChatBot
from wxmodel import reply, receive
from wxcrypt.WXBizMsgCrypt import WXBizMsgCrypt
from datetime import datetime
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')

class ThirdPartHandle(object):
    def __init__(self):
        wx_config = gl.get_value('config')['wechat_thirdpart']
        self.wxMsgCrypt = WXBizMsgCrypt(str(wx_config['token']),
                                        str(wx_config['encodingAESKey']),
                                        str(wx_config['appId']))

    def msgEncryt(self, replymsg):
        gl.getLogger().debug(replymsg)
        ret, encrypt_xml = self.wxMsgCrypt.EncryptMsg(replymsg, web.input().nonce)
        # print(encrypt_xml)
        return encrypt_xml

    def msgDecrypt(self, urlParam, bodyData):
        # print(urlParam)
        # print(bodyData)
        ret, decrypt_xml = self.wxMsgCrypt.DecryptMsg(bodyData, str(urlParam.msg_signature), str(urlParam.timestamp), str(urlParam.nonce))
        gl.getLogger().debug(decrypt_xml)
        return receive.parse_xml(decrypt_xml)


    def POST(self, client_id):
        try:
            print("from client:%s" % client_id)
            recMsg = self.msgDecrypt(web.input(), web.data())

            toUser = recMsg.FromUserName
            fromUser = recMsg.ToUserName

            if isinstance(recMsg, receive.Msg):
                # 机器人闲聊
                if recMsg.MsgType == 'text':
                    gl.getLogger().info("text:[client_id:\"%s\",open_id:\"%s\",text:\"%s\"]" % (client_id, toUser, recMsg.Content))
                    db = gl.get_value("mongodb")
                    result = db.wechatoffical_chatbot.find_one({"app_id": str(client_id)})
                    if None != result and result.has_key('auto_reply') and  1 == result['auto_reply']:
                        if "【收到不支持的消息类型，暂无法显示】" == recMsg.Content:
                            # 收到表情消息时,微信服务器推送此消息过来,使用默认回复处理
                            content = None
                        else:
                            content = tulingChatBot.replyTextMsg(recMsg.Content, toUser)

                        if None == content and result.has_key('default_reply') and '' != result['default_reply']:
                            content = result['default_reply']

                        if content != None:
                            replyMsg = reply.TextMsg(toUser, fromUser, content)
                            gl.getLogger().info("text_reply:[client_id:\"%s\",open_id:\"%s\",reply:\"%s\"]" % (client_id, toUser, content))
                            db.wechatoffical_chatbot_history.insert({"app_id":client_id, "open_id":toUser, "say":recMsg.Content, "reply":content, "creation_time":datetime.now()})
                            return self.msgEncryt(replyMsg.send())

                # 图片消息
                if recMsg.MsgType == 'image':
                    mediaId = recMsg.MediaId
                    gl.getLogger().info("image:[client_id:\"%s\",open_id:\"%s\", MediaId:\"%s\"]" % (client_id, toUser, mediaId))
                    # replyMsg = reply.ImageMsg(toUser, fromUser, mediaId)
                    # return self.msgEncryt(replyMsg.send())

                # 视频消息
                if recMsg.MsgType == 'video':
                    mediaId = recMsg.MediaId
                    thumbMediaId = recMsg.ThumbMediaId
                    gl.getLogger().info("video:[client_id:\"%s\",open_id:\"%s\", MediaId:\"%s\",ThumbMediaId:\"%s\"]" % (client_id, toUser, mediaId, thumbMediaId))

            if isinstance(recMsg, receive.EventMsg):
                # 被关注自动回复
                if recMsg.Event == 'subscribe':
                    gl.getLogger().info("subscribe:[client_id:\"%s\",open_id:\"%s\"]" % (client_id, toUser))
                    db = gl.get_value("mongodb")
                    result = db.wechatoffical_chatbot.find_one({"app_id": str(client_id)})
                    if None != result and result.has_key('auto_reply') and 1 == result['auto_reply'] and result.has_key('followed_reply') and '' != result['followed_reply']:
                        content = result['followed_reply']
                        replyMsg = reply.TextMsg(toUser, fromUser, content)
                        gl.getLogger().info("subscribe:[client_id:\"%s\",open_id:\"%s\",reply:\"%s\"]" % (client_id, toUser, content))
                        return self.msgEncryt(replyMsg.send())

                # 取消关注
                if recMsg.Event == 'unsubscribe':
                    gl.getLogger().info("unsubscribe:[client_id:\"%s\",open_id:\"%s\"]" % (client_id, toUser))

            return reply.Msg().send()

        except Exception, Argment:
            gl.getLogger().error(traceback.format_exc())
            return reply.Msg().send()
