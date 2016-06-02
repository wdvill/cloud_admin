#-*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement
import os
from common import utils
import datetime


TR_CN = None
TR_EN = None

def timediff_format(value, fmt="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.strptime(value, fmt)
    now = utils.now()
    delta = now - dt
    seconds = delta.total_seconds()
    if seconds < 60:
        return "%s second ago" % seconds
    if seconds >= 60 and seconds < 3600:
        return "%s minute ago" % int(seconds / 60)
    if seconds >= 3600 and seconds < 86400:
        return "%s hour ago" % int(seconds / 3600)
    if seconds >= 86400 and seconds < 2592000:
        return "%s day ago" % int(seconds / 86400)
    if seconds >= 2592000 and seconds < 31104000:
        return "%s month ago" % int(seconds / 2592000)
    return "%s year ago" % int(seconds / 31104000)

def trans(value, lang="en_US", key=None):
    if lang == "en_US":
        if key:
            return TR_EN[key][str(value)]
        return TR_EN[value]
    if lang == "zh_CN":
        if key:
            return TR_CN[key][str(value)]
        return TR_CN[value]

def trans_time(value, lang="en_US"):
    if lang == "en_US":
        return value
    return "%s%s" % (value.split(" ")[0], TR_CN[" ".join(value.split(" ")[1:])])
