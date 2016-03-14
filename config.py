#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CORP ID AND SECRET INFO

CORP_INFO = {
    "corpid": "Your corpid here",
    "secret": "Your secret here"
}

# MESSAGE CONFIGURATION

MESSAGE_CONF = {
    "touser": "@all",
    "toparty": "",
    "totag": "",
    "msgtype": "text",
    "agentid": "0",
    "text": {
        "content": ""
    },
    "safe": "0"
}

# TOKEN FILE PATH (default: /tmp/token.json)

TOKEN_PATH = r'/tmp/token.json'

# LOG FILE PATH (default: /var/log/asterisk/smsgateway.log)

LOG_PATH = r'/var/log/asterisk/smsgateway.log'
