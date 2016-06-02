#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import requests
import traceback
import logging
from config import settings
from common import utils

logger = logging.getLogger("idverify")

def id_verify_remote(name, id_number):
    if settings.debug:
        return True

    url = "%s?name=%s&cardno=%s" % (settings.idverify.uri, name, id_number)
    header = {"apikey":settings.idverify.key, "user-agent":"yunzujia remote httplib"}
    res = requests.get(url, headers=header)
    logger.error("%s" % res.content)
    if res.status_code != 200:
        return False
    try:
        content = utils.loads(res.content)
        if content['code'] == 0:
            return True
    except:
        logger.error(traceback.format_exc())
    return False
