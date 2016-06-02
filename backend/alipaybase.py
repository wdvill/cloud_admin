#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import requests

from alipay import Alipay
from config.settings import alipay_config, debug


class AlipayBase(Alipay):
    """ add debug url """

    def __init__(self):
        self.GATEWAY_URL = alipay_config["gateway_url"]
        self.NOTIFY_GATEWAY_URL = self.GATEWAY_URL + "?service=notify_verify&partner=%s&notify_id=%s"
        pid = alipay_config["partner"]
        key = alipay_config["key"]
        seller_email = alipay_config["seller"]
        super(AlipayBase, self).__init__(pid=pid, key=key, seller_email=seller_email)

    def check_notify_remotely(self, **kw):
        verify = not debug
        remote_result = requests.get(
            self.NOTIFY_GATEWAY_URL % (self.pid, kw['notify_id']),
            headers={'connection': 'close'},
            verify=verify
        ).text
        return remote_result == 'true'
