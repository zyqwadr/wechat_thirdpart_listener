# -*- coding: utf-8 -*-
# filename: main.py

import json
import pprint
import web
import globalvar as gl
from sys import argv
from router.testurl import Testurl
from router.handle import Handle
from router.thirdPartHandle import ThirdPartHandle
import logging
import pymongo
import logging.config

urls = (
    '/wx', 'Handle',
    '/wechat/thirdpart/events/listen/(.*?)', 'ThirdPartHandle',
    '/test', 'Testurl'
)

if __name__ == '__main__':

    gl._init()

    # logger config
    logging.config.fileConfig("config/logger.conf")
    logger = logging.getLogger("example01")
    gl.set_value('logger', logger)

    # env config
    ENV = 'dev'
    if len(argv) > 2 and argv[2] in ('dev','test','prod'):
        ENV = argv[2]
    CONFIG = json.load(open('config/config.json'))[ENV]
    logger.debug("run environment: %s" % (ENV))
    logger.debug("run config: %s" % (CONFIG))

    gl.set_value('env', ENV)
    gl.set_value('config', CONFIG)
    uri = "mongodb://%s:%s@%s:%s/%s?authMechanism=SCRAM-SHA-1" % (CONFIG['mongodb']['username'],CONFIG['mongodb']['password'],CONFIG['mongodb']['host'],CONFIG['mongodb']['port'],CONFIG['mongodb']['db'])
    print(uri)
    client = pymongo.MongoClient(uri)
    db = client[CONFIG['mongodb']['db']]
    gl.set_value('mongodb', db)

    result = db.wechatoffical_chatbot.count({"auto_reply":1})
    print("total chatbot user count:"+str(result))

    app = web.application(urls, globals())
    print("App Started. ENV:" + ENV)
    app.run()
