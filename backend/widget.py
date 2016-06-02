#!/usr/bin/env python
# -*- coding:utf-8 -*-

from __future__ import absolute_import, division, print_function, with_statement

import random
from config.settings import qiniu_key, host, cache

def avatar(value=""):
    if not value:
        return "/static/images/default-avatar0%s.png" % random.randint(1,8)
    if value.startswith("/static"):
        return "%s%s" % (host, value)
    return "%s/%s" % (qiniu_key.uri, value)

def logo(value=""):
    if not value:
        return "/static/images/default-avatar0%s.png" % random.randint(1,8)

    #if hasattr(value, "logo"):
    #    if value.logo == "":
    #        return ""
    #    return "%s/%s" % (qiniu_key.uri, value.logo)

    if value.startswith("/static"):
        return "%s%s" % (host, value)
    return "%s/%s" % (qiniu_key.uri, value)

def picture(value):
    if not value:
        return ""
    return "%s/%s" % (qiniu_key.uri, value)

def attach(value):
    if not value:
        return ""
    return "%s/%s" % (qiniu_key.uri, value)

def get_category(cid):
    return cache.get("category_%s" % cid)

def get_location(lid):
    return cache.get("address_%s" % lid)
