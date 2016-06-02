#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, with_statement

import re

RE_USERNAME = r"^[a-zA-z]\w{3,19}$"
RE_EMAIL = r"^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$"
RE_VERIFY_CODE = r"\d{6}$"
RE_PASSWORD = r"^[A-Za-z0-9_]{6,20}$"

# 手机号码: 13[0-9], 14[5,7], 15[0, 1, 2, 3, 5, 6, 7, 8, 9], 17[6, 7, 8], 18[0-9], 170[0-9]
RE_PHONE = r"^1(3[0-9]|4[57]|5[0-35-9]|8[0-9]|7[0-9])\d{8}$"


def is_name(words):
    if re.match(RE_USERNAME, words):
        return True
    return False

def is_phone(words):
    if re.match(RE_PHONE, words):
        return True
    return False

def is_email(words):
    if re.match(RE_EMAIL, words):
        return True
    return False

def is_verify_code(words):
    if re.match(RE_VERIFY_CODE, words):
        return True
    return False

def is_password(words):
    if re.match(RE_PASSWORD, words):
        return True
    return False

def is_username(words):
    if is_name(words) or is_phone(words) or is_email(words):
        return True
    return False

def login(username):
    if is_username(username):
        return True
    return False

def forget_password(username, vcode):
    if is_username(username) and is_verify_code(vcode):
        return True
    return False

def register(phone, vcode, name):
    pass
