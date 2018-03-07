# -*- coding: utf-8 -*-

import pprint
import globalvar as gl
import json
import web
import threading
import sys
import traceback
reload(sys)
sys.setdefaultencoding('utf-8')

class Testurl(object):
    def __init__(self):
        thread = threading.current_thread()
        print("Init Testurl "+thread.getName())

    def GET(self):
        try:
            thread = threading.current_thread()
            print("GET " + thread.getName())
            web.header('Content-Type', 'application/json')
            gl.getLogger().debug('This is debug message')
            db = gl.get_value("mongodb")
            result = db.wechatoffical_chatbot.find_one({"app_id": "d"})
            print(result)
            print(result['auto_reply'])
            print(result['default_reply'])
            print(gl.get_value('env'))
            return json.dumps(gl.get_value('config'))
        except Exception, Argument:
            gl.getLogger().error(traceback.format_exc())
            return Argument

    def POST(self):
        try:
            thread = threading.current_thread()
            print("POST " + thread.getName())
            web.header('Content-Type', 'application/json')
            gl.getLogger().debug('This is debug message')
            print(gl.get_value('env'))
            return json.dumps(gl.get_value('config'))
        except Exception, Argument:
            return Argument
