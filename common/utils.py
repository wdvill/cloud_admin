#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import sys
import time
import datetime
import hashlib
import re
import random
try:
    import ujson as json
except:
    import json 
import decimal


utc_offset = time.timezone

#UTC时间戳
def stamp():
    return int(time.time() + utc_offset)

#UTC时间
def now():
    return datetime.datetime.fromtimestamp(time.time() + utc_offset)

def local_datetime(dt):
    """
        The parameter 'dt' must be utc datetime
    """
    return dt - datetime.timedelta(seconds=utc_offset)

def localtime(stamp):
    """
        The parameter 'stamp' must be utc timestamp
    """
    return stamp - utc_offset

def utc_datetime(dt):
    """
        local datetime convert to utc
    """
    return dt + datetime.timedelta(seconds=utc_offset)

def timedelta(dt, days=0):
    return dt + datetime.timedelta(days=days)

def utctime(stamp):
    """
        local timestamp convert to utc
    """
    return stamp + utc_offset

def rand_str(num=10):
    return "".join(random.sample("ABCDEFGHJKLMNPQRSTUVWXY23456789ABCDEFGHJKLMNPQRSTUVWXY23456789abcdefghjkmnpqrstuvwxy23456789abcdefghjkmnpqrstuvwxy23456789", num))

def rand_num():
    return "%06d" % random.randint(100000, 999999)

def md5(s):
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()

def local_datetime_to_str(dt):
    """
        The parameter 'dt' must be utc datetime from database
    """
    if not dt:
        return ""
    return local_datetime(dt).strftime('%Y-%m-%d %H:%M:%S')

def str_to_datetime(dt_str, pattern="%Y-%m-%d %H:%M:%S", utc=True):
    try:
        dt = datetime.datetime.strptime(dt_str, pattern)
        if utc:
            return utc_datetime(dt)
        return dt
    except:
        return None

def str_to_date(dt_str, utc=True):
    return str_to_datetime(dt_str, pattern="%Y-%m-%d", utc=utc)

def datetime_to_date(dt):
    if not dt:
        return ""
    return local_datetime(dt).strftime('%Y-%m-%d')

def datetime_to_str(dt):
    if not dt:
        return ""
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def datetime_to_number(dt):
    return dt.strftime("%Y%m%d%H%M%S")

def datetime_to_day_number(dt):
    return dt.strftime("%Y%m%d")

def datetime_day_min(dt, utc=True):
    if utc:
        return datetime.datetime(dt.year, dt.month, dt.day, 16, 0, 0) + datetime.timedelta(days=-1)
    return datetime.datetime(dt.year, dt.month, dt.day, 0, 0, 0) + datetime.timedelta(seconds=utc_offset)

def datetime_day_max(dt, utc=True):
    if utc:
        return datetime.datetime(dt.year, dt.month, dt.day, 15, 59, 59)
    return datetime.datetime(dt.year, dt.month, dt.day, 23, 59, 59) + datetime.timedelta(seconds=utc_offset)

def datetime_interval(dt):
    minute = dt.minute
    second = dt.second
    minute_start = int(minute / 10) * 10
    minute_end = minute_start + 9

    m = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, minute_start, 0)
    l = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, minute_end, 59)
    return m, l


def valid_special_characters(s):
    pattern = re.compile(br"[@,;']")
    if isinstance(s, str):
        s = s.encode(encoding="utf-8")
    results = re.search(pattern, s)
    if results:
        return False
    return s

def dumps(dic):
    return json.dumps(dic, ensure_ascii=False, indent=2)

def loads(source):
    return json.loads(source)

def safe_id(value):
    try:
        return int(value)
    except Exception:
        return False

def encode_html(content):
    content = content.replace("<", "&lt;")
    content = content.replace(">", "&gt;")
    content = content.replace("&", "&amp;")
    return content

def decimal_two(value):
    try:
        value = decimal.Decimal(value)
        return value.quantize(decimal.Decimal("0.01"), rounding=decimal.ROUND_DOWN)
    except:
        return None

def generate_id():
    s = "%s%s" % (long(time.time() * 10000), rand_str())
    return md5(s)[8:24]

def isLocalMobile(num):
    if re.match("^((13[0-9])|(15[^4,\\D])|(14[5,7])|(17[0,7,8])|(18[^4,\\D]))\\d{8}$", num):
        return True
    return False

def is_username(name):
    if re.match(r"^[a-zA-z0-9]{3,19}$", name):
        return True
    return False

#解析user-agent
def resolve_agent(agent):
    """i/1.0.0/9.2.1/iPhone/wifi"""
    """a/1.0.0/6.0.1/Sumsang S6/3g"""
    if agent[:2] not in ("i/", "a/", "w/"):
        return None
    arr = agent.split("/")
    if len(arr) < 5:
        return None
    #TODO return value
    return {"os":arr[0], "app_version":arr[1], 
            "os_version": arr[2], "device": arr[3],
            "network": arr[4]}

def get_domain(host):
    host = host.split(":")[0]
    if ".com.cn" in host or ".net.cn" in host:
        domain = ".".join(host.split(".")[-3:])
    elif ".net" in host or ".com" in host:
        domain = ".".join(host.split(".")[-2:])
    else:
        domain = ""
    return domain


def lang_map_name(name, ename, lang="zh_CN"):
    """ name: chinese name
        ename: english name
        lang: language type
    """
    if lang == "zh_CN":
        return name
    return ename

def replace_html_tag(s):
    p = re.compile('<[^>]+>')
    return p.sub("", s)
