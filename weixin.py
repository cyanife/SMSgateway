#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import os
import sys
import time
import json
import logging
import logging.handlers

reload(sys)
sys.setdefaultencoding('utf-8')


class AccessToken(object):
    def __init__(self):
        self.path = ""
        self.corpid = ""
        self.secret = ""

    def setpath(self, path):
        self.path = path

    def setcorpid(self, corpid):
        self.corpid = corpid

    def setsecret(self, secret):
        self.secret = secret

    def getcorpinfo(self):
        try:
            with open(os.path.join(self.path, "corpinfo.conf"), 'r') as f:
                info_dict = json.loads(f.read())
                self.setcorpid(info_dict.get("corpid"))
                self.setsecret(info_dict.get("secret"))
        except IOError:
            print("get info failed, check the file!")

    def settoken(self):
        if self.corpid == '' or self.secret == '':
            raise ValueError("invalid Corpid or Secret!")
        tokenapi = urllib2.urlopen(
            "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (self.corpid, self.secret))
        token_dict = json.loads(tokenapi.read())
        token_dict["expires_at"] = str(time.time() + 7000)
        if token_dict.get("access_token") == "":
            print("Error Code:%s, %s" % (token_dict.get("errcode"), token_dict.get("errmsg")))
            raise ValueError
        with open(os.path.join(self.path, "Token.json"), 'w') as fw:
            json.dump(token_dict, fw)

    def gettoken(self):
        success = False
        token_dict = {}
        while not success:
            try:
                with open(os.path.join(self.path, "Token.json")) as fr:
                    token_file = fr.read()
                    if token_file == "":
                        self.settoken()
                    else:
                        token_dict = json.loads(token_file)
                        if str(time.time()) > token_dict.get("expires_at"):
                            self.settoken()
                        else:
                            success = True
            except IOError:
                self.settoken()
        return token_dict.get("access_token")


class Activemessage(object):
    def __init__(self, message):
        self.touser = message.pop("touser", None)
        self.toparty = message.pop("toparty", None)
        self.totag = message.pop("totag", None)
        self.agentid = message.pop("agentid", 0)

    def update(self, message):
        self.__dict__.update(message)

    def sendmessage(self, token):
        message = json.dumps(self.__dict__, ensure_ascii=False)
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % (token,)
        request = urllib2.Request(url, message)
        response = urllib2.urlopen(request)
        result = json.loads(response.read())
        return result


class Textmessage(Activemessage):
    def __init__(self, message):
        super(Textmessage, self).__init__(message)
        self.msgtype = "text"
        self.text = message.pop("text", None)
        self.safe = message.pop("safe", 0)

    def setcontent(self, content):
        text = {"content": content}
        self.text = text

    def loadmessage(self, filename):
        try:
            with open(filename, 'r') as f:
                message = json.load(f)
                self.update(message)
        except IOError:
            print("Failed to load message from file!")


class Parseargv(object):
    def __init__(self, argv):
        self.sender = argv[1]  # sender's phone number
        self.time_received = argv[2]  # time received
        self.sms_content = argv[3]  # content


def main():
    # Setup logger
    LOG_PATH = r"C:\myfiles\nutstore\python\smsgateway\smsgateway.log"
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s %(levelname)s] %(message)s')
    handler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=1)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    # Get token
    tk = AccessToken()
    tk.setpath(os.getcwd())
    tk.getcorpinfo()
    token = tk.gettoken()
    # Send message
    message_conf = os.path.join(os.getcwd(), 'message.conf')
    BLANK_MESSAGE = {}
    msg = Textmessage(BLANK_MESSAGE)
    msg.loadmessage(message_conf)
    argv = Parseargv(sys.argv)
    # msg.setcontent(unicode("hybird测试"))
    # msg.setcontent(sys.argv[1].decode("GBK"))  # windows console下，参数编码为GBK
    msg.setcontent("%s\nFrom:%s\nTime:%s" % (argv.sms_content, argv.sender, argv.time_received))
    # msg.setcontent(sys.argv[1])  # linux下，参数编码为UTF8
    result = msg.sendmessage(token)
    errcode = result.pop("errcode", 1)
    if errcode == 0:
        logger.info("SENDER:%s TIME:%s CONTENT:%s FORWARD:%s" % (argv.sender, argv.time_received, argv.sms_content,
                                                                 'SUCCESS'))
    else:
        logger.error("SENDER:%s TIME:%s CONTENT:%s FORWARD:%s ERRINFO:" % (argv.sender, argv.time_received,
                                                                           argv.sms_content, 'FAIL', result))
        # print result


if __name__ == '__main__':
    main()
