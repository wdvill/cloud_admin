# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import requests
from config.settings import baiwu
from common import utils


class BaiWuTong(object):

    def send(self, phone, text):
        return self.send_messages(phones=[phone], messages=text)

    def send_messages(self, phones, messages):
        if not isinstance(phones, list) or len(phones) == 0 or len(phones) > 200:
            return False, "phone list length invalid"

        if len(messages) == 0 or len(messages) > 1000:
            return False, "message length length invalid"

        phones = [str(phone) for phone in phones]
        data = {
            "id": baiwu["client_id"],
            "MD5_td_code": utils.md5(baiwu["password"] + baiwu["code"]),
            "mobile": ",".join(phones),
            "msg_content": messages,
            "msg_id": "",
            "ext": ""
        }
        headers = {'content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
        try:
            rps = requests.post(baiwu["uri"], data=data, headers=headers)
            error_code, msg = rps.status_code, str(rps.text)
            if error_code == 200 and msg[:1] == "0":
                return True, "success request:%s" % rps.text
            return False, "fail request:%s" % rps.text
        except:
            return False, "fail request: connect failed"
